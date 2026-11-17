import sqlite3
import ast
from groq import Groq

# 1. Defining Model and API key
API_KEY = "GetOnOneDrive"
MODEL_NAME = "openai/gpt-oss-120b" 

client = Groq(api_key=API_KEY)
conn = sqlite3.connect('errorease.db')
cursor = conn.cursor()

# Enable foreign keys for the new tables
cursor.execute('PRAGMA foreign_keys = ON')

# Create the NEW AI tables for testing
cursor.execute('''
    CREATE TABLE IF NOT EXISTS AI_ERRORS (
        ErrorCode TEXT PRIMARY KEY,
        ErrorName TEXT,
        ErrorDescription TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS AI_SOLUTIONS (
        SolutionID INTEGER PRIMARY KEY AUTOINCREMENT,
        ErrorCode TEXT NOT NULL,
        PlainEnglishSummary TEXT,
        StepByStepFix TEXT,
        Upvotes INTEGER DEFAULT 0,
        Downvotes INTEGER DEFAULT 0,
        FOREIGN KEY (ErrorCode) REFERENCES AI_ERRORS(ErrorCode)
    )
''')

# 2. GET USER INPUT AND CLEAN IT
print("="*50)
print(" ERROREASE SEARCH")
print("="*50)

error_code = input("Enter a Windows error code (e.g., 0x80070005): ").strip()

if error_code and not error_code.lower().startswith('0x'):
    if all(c in "0123456789abcdefABCDEF" for c in error_code):
        error_code = "0x" + error_code

# 3. Check ORIGINAL Database first
query = """
    SELECT ERRORS.ErrorName, ERRORS.ErrorDescription, SOLUTIONS.PlainEnglishSummary, SOLUTIONS.StepByStepFix, SOLUTIONS.Upvotes, SOLUTIONS.Downvotes
    FROM SOLUTIONS
    JOIN ERRORS ON SOLUTIONS.ErrorCode = ERRORS.ErrorCode
    WHERE SOLUTIONS.ErrorCode = ?
"""
cursor.execute(query, (error_code,))
results = cursor.fetchall()

# 4. IF FOUND IN ORIGINAL DATABASE
if results:
    print(f"\n✅ Error found in your original 'errorease.db'!")
    print(f"Error Name: {results[0][0]}")
    print(f"Description: {results[0][1]}\n")
    print("Available Solutions:")
    print("-" * 40)
    for row in results:
        print(f"Summary: {row[2]}")
        print(f"Fix: {row[3]}")
        print(f"Upvotes: {row[4]} | Downvotes: {row[5]}")
        print("-" * 40)

# 5. IF NOT FOUND IN ORIGINAL DATABASE
else:
    # First, check if it's just random text/tricks (doesn't start with 0x)
    if not error_code.lower().startswith('0x'):
        print("\nInvalid inputs, errors only!")
    else:
        # Check if it's ALREADY in the AI tables
        cursor.execute("SELECT * FROM AI_ERRORS WHERE ErrorCode = ?", (error_code,))
        ai_exists = cursor.fetchone()

        if ai_exists:
            print(f"\n✅ Error found in your 'AI_ERRORS' table!")
            print(f"Error Name: {ai_exists[1]}")
            print(f"Description: {ai_exists[2]}\n")
            
            cursor.execute("SELECT * FROM AI_SOLUTIONS WHERE ErrorCode = ?", (error_code,))
            ai_solutions = cursor.fetchall()
            for row in ai_solutions:
                print(f"Summary: {row[2]}")
                print(f"Fix: {row[3]}")
                print(f"Upvotes: {row[4]} | Downvotes: {row[5]}")
                print("-" * 40)
        else:
            # It's not in the original DB, and not in the AI DB. Ask the AI!
            print(f"\n⚠️ Error is new! Asking AI to generate data for '{error_code}'...")
            print("🤖 AI is thinking...\n")
            
            prompt = f"""
            Check if the Windows error code {error_code} is a real, documented Windows error.
            - If it is FAKE or NOT REAL, reply ONLY with the exact text: Error is invalid!
            - If it IS real, reply ONLY with a Python tuple in this exact 7-item format. 
              Do not add any extra words, greetings, or markdown code blocks.
              ('{error_code}', 'ErrorName', 'One sentence description', 'Short Summary', '1 to 3 step fix', 0, 0)
            """

            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a strict data-entry bot. You only output the exact requested format."},
                        {"role": "user", "content": prompt}
                    ],
                    model=MODEL_NAME
                )
                
                ai_response = chat_completion.choices[0].message.content.strip()
                if ai_response.startswith("```"):
                    ai_response = ai_response.strip("`").replace("python", "").strip()
                
                if ai_response == "Error is invalid!":
                    print(f"\n{ai_response}")
                else:
                    new_data = ast.literal_eval(ai_response)
                    
                    # Save to AI tables
                    cursor.execute('INSERT OR IGNORE INTO AI_ERRORS (ErrorCode, ErrorName, ErrorDescription) VALUES (?, ?, ?)', (new_data[0], new_data[1], new_data[2]))
                    
                    # UPDATED: Prevents saving the exact same fix twice!
                    cursor.execute('''
                        INSERT INTO AI_SOLUTIONS (ErrorCode, PlainEnglishSummary, StepByStepFix, Upvotes, Downvotes)
                        SELECT ?, ?, ?, ?, ?
                        WHERE NOT EXISTS (SELECT 1 FROM AI_SOLUTIONS WHERE ErrorCode = ? AND StepByStepFix = ?)
                    ''', (new_data[0], new_data[3], new_data[4], new_data[5], new_data[6], new_data[0], new_data[4]))
                    
                    conn.commit()
                    
                    print("💾 Successfully saved to AI_ERRORS and AI_SOLUTIONS tables!")
                    print(f"\nSummary: {new_data[3]}")
                    print(f"Fix: {new_data[4]}")
                    print(f"Upvotes: {new_data[5]} | Downvotes: {new_data[6]}")
                    print("-" * 40)
                    
            except Exception as e:
                print(f"\n❌ AI Error: {e}")

conn.close()