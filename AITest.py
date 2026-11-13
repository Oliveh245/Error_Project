import sqlite3
from groq import Groq

# 1. Defining Model and API key, please keep it a secret
API_KEY = "CheckOnedrive"
MODEL_NAME = "openai/gpt-oss-120b" 

client = Groq(api_key=API_KEY)
conn = sqlite3.connect('errorease.db')
cursor = conn.cursor()

# 2. GET USER INPUT AND CLEAN IT
print("="*50)
print(" ERROREASE SEARCH")
print("="*50)

error_code = input("Enter a Windows error code (e.g., 0x80070005): ").strip()

# Smart check: If it's not empty and doesn't start with '0x', let's add it!
if error_code and not error_code.lower().startswith('0x'):
    # Check if it looks like a hex number (only contains numbers and letters A-F)
    if all(c in "0123456789abcdefABCDEF" for c in error_code):
        error_code = "0x" + error_code

# 3. Open ErroreaseDB first to check
query = """
    SELECT ERRORS.ErrorName, ERRORS.ErrorDescription, SOLUTIONS.PlainEnglishSummary, SOLUTIONS.StepByStepFix, SOLUTIONS.Upvotes, SOLUTIONS.Downvotes
    FROM SOLUTIONS
    JOIN ERRORS ON SOLUTIONS.ErrorCode = ERRORS.ErrorCode
    WHERE SOLUTIONS.ErrorCode = ?
"""
cursor.execute(query, (error_code,))
results = cursor.fetchall()

# 4. IF FOUND IN DATABASE
if results:
    print(f"\n✅ Error found in your 'errorease.db'!")
    print(f"Error Name: {results[0][0]}")
    print(f"Description: {results[0][1]}\n")
    print("Available Solutions:")
    print("-" * 40)
    
    for row in results:
        print(f"Summary: {row[2]}")
        print(f"Fix: {row[3]}")
        print(f"Upvotes: {row[4]} | Downvotes: {row[5]}")
        print("-" * 40)

# 5. IF NOT FOUND IN DATABASE
else:
    # First, check if it's just random text/tricks (doesn't start with 0x)
    if not error_code.lower().startswith('0x'):
        print("\nInvalid inputs, errors only!")
    else:
        # It starts with 0x, so it looks like an error. Let the AI fact-check it!
        print("\n🤖 AI is fact-checking this error code...")
        
        # We tell the AI to ONLY give us the description, or say it's invalid.
        prompt = f"""
        Check if the Windows error code {error_code} is a real, documented Windows error.
        - If it is FAKE or NOT REAL, reply ONLY with the exact text: Error is invalid!
        - If it IS real, reply ONLY with a one simple sentence description of the error. Do not include the error code in your reply.
        """

        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a strict validation bot. You only output the exact requested format. No pleasantries."
                    },
                    {"role": "user", "content": prompt}
                ],
                model=MODEL_NAME
            )
            
            
            ai_response = chat_completion.choices[0].message.content.strip()
            
            
            if ai_response == "Error is invalid!":
                print(f"\n{ai_response}")
            else:
                
                print(f"\nError Code: {error_code}")
                print(f"Description: {ai_response}")
                
        except Exception as e:
            print(f"\n❌ AI Error: {e}")


conn.close()