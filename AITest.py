import sqlite3
import ast
from groq import Groq

#FUNCTION DEFINITIONS
# Displays the new error and solution in console on join using origianl tables. ACTUAL
def display_error_and_solutions(cursor, error_code):        
    cursor.execute("""
        SELECT ERRORS.ErrorCode,
               ERRORS.ErrorDescription,
               SOLUTIONS.PlainEnglishSummary,
               SOLUTIONS.StepByStepFix
        FROM ERRORS
        JOIN SOLUTIONS
        ON ERRORS.ErrorCode = SOLUTIONS.ErrorCode
        WHERE ERRORS.ErrorCode = ?
    """, (error_code,))

    results = cursor.fetchall()

    for row in results:
        print("Error Code:", row[0])
        print("Error Description:", row[1])
        print("Summary:", row[2])
        print("Solution:", row[3])

#Displays the new error and solution in console on join using new tables. TESTING
# def display_error_and_solutions(cursor, error_code):        
#     cursor.execute("""
#         SELECT AI_ERRORS.ErrorCode,
#             AI_ERRORS.ErrorDescription,
#             AI_SOLUTIONS.PlainEnglishSummary,
#             AI_SOLUTIONS.StepByStepFix
#         FROM AI_ERRORS
#         JOIN AI_SOLUTIONS
#         ON AI_ERRORS.ErrorCode = AI_SOLUTIONS.ErrorCode
#         WHERE AI_ERRORS.ErrorCode = ?
#     """, (error_code,))

#     results = cursor.fetchall()

#     for row in results:
#         print("Error Code:", row[0])
#         print("Error Description:", row[1])
#         print("Summary:", row[2])
#         print("Solution:", row[3])

#Insers the new data from the AI into the original tables. ACTUAL
def insert_new_data(cursor, new_data):
    try:
        cursor.execute('INSERT OR IGNORE INTO ERRORS (ErrorCode, ErrorName, ErrorDescription) VALUES (?, ?, ?)', (new_data[0], new_data[1], new_data[2]))
        cursor.execute('''
            INSERT INTO SOLUTIONS (ErrorCode, PlainEnglishSummary, StepByStepFix, Upvotes, Downvotes)
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM SOLUTIONS WHERE ErrorCode = ? AND StepByStepFix = ?)
        ''', (new_data[0], new_data[3], new_data[4], new_data[5], new_data[6], new_data[0], new_data[4]))

        if cursor.rowcount > 0:
            cursor.connection.commit()
            return True
        else:
            cursor.connection.commit()
            print("No new data inserted; the solution already exists.")
            return False
        
    except Exception as e:
        cursor.connection.rollback()
        print(f"Database error: {e}")
        return False

#Insers the new data from the AI into the AI tables. TESTING
# def insert_new_data(cursor, new_data):
#     try:
#         cursor.execute('INSERT OR IGNORE INTO AI_ERRORS (ErrorCode, ErrorName, ErrorDescription) VALUES (?, ?, ?)', (new_data[0], new_data[1], new_data[2]))
#         cursor.execute('''
#             INSERT INTO AI_SOLUTIONS (ErrorCode, PlainEnglishSummary, StepByStepFix, Upvotes, Downvotes)
#             SELECT ?, ?, ?, ?, ?
#             WHERE NOT EXISTS (SELECT 1 FROM AI_SOLUTIONS WHERE ErrorCode = ? AND StepByStepFix = ?)
#         ''', (new_data[0], new_data[3], new_data[4], new_data[5], new_data[6], new_data[0], new_data[4]))

#         if cursor.rowcount > 0:
#             cursor.connection.commit()
#             return True
#         else:
#             cursor.connection.commit()
#             print("No new data inserted; the solution already exists.")
#             return False
        
#     except Exception as e:
#         cursor.connection.rollback()
#         print(f"Database error: {e}")
#         return False

#creating and using AI model to search error code and generate a solution to go along with it.
def create_ai_solutions(cursor, error_code):
    print(f"\n⚠️ Error is new! Asking AI to generate data for '{error_code}'...")
    print("🤖 AI is thinking...\n")

    #Checks if there are already existing solutions for the error code in the AI_SOLUTIONS table and stores them to not make duplicates
    cursor.execute("""
    SELECT PlainEnglishSummary
    FROM SOLUTIONS
    WHERE ErrorCode = ?
    """, (error_code,))
    existing_summaries = [row[0] for row in cursor.fetchall()]

    #NEW PROMPT
    prompt = f"""
    Check if the Windows error code {error_code} is a real, documented Windows error.
    - If it is FAKE or NOT REAL, reply ONLY with the exact text: Error is invalid!
    - If it IS real, reply ONLY with a Python tuple in this exact 7-item format:
        ('{error_code}', 'ErrorName', 'One sentence description', 'One sentence summary of the 1 to 3 step fix', '1 to 3 step fix', 0, 0)

    IMPORTANT: The following solutions already exist for this error code:
    {existing_summaries if existing_summaries else "No existing solutions."}
    Your new solution MUST:
    - Provide a genuinely different troubleshooting approach.
    - Not repeat the same underlying fix as an existing solution.
    - Not simply reword an existing solution.
    - Use a different troubleshooting method, tool, or repair approach where possible.
    - Avoid repeating the same steps in a different order.
    If no genuinely different solution can be suggested, reply ONLY with:
    No new solution available!
    Do not add extra words, greetings, or markdown code blocks.
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
            return False
        elif ai_response == "No new solution available!":
            print(f"\n{ai_response}")
            return False
        else:
            new_data = ast.literal_eval(ai_response)

            #Makes sure the AI response is in the correct format before inserting into the database
            if not isinstance(new_data, tuple) or len(new_data) != 7:
                print("Invalid AI response format.")
                return False

            # If it comes back True then it was safely inserted into the table as a new solution
            isWorking = insert_new_data(cursor, new_data)
            if not isWorking:
                return False
            else:
                return True
    except Exception as e:
        print(f"\nAI Error: {e}")
        return False
#END OF FUNCTIONS

# 1. Defining Model and API key
API_KEY = "OneDriveKey"
MODEL_NAME = "openai/gpt-oss-120b" 

client = Groq(api_key=API_KEY)
conn = sqlite3.connect('errorease.db')
cursor = conn.cursor()

# Enable foreign keys for the new tables
cursor.execute('PRAGMA foreign_keys = ON')

# Create the NEW AI tables for testing. DELETE WHEN DONE TESTING
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS AI_ERRORS (
#         ErrorCode TEXT PRIMARY KEY,
#         ErrorName TEXT,
#         ErrorDescription TEXT
#     )
# ''')
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS AI_SOLUTIONS (
#         SolutionID INTEGER PRIMARY KEY AUTOINCREMENT,
#         ErrorCode TEXT NOT NULL,
#         PlainEnglishSummary TEXT,
#         StepByStepFix TEXT,
#         Upvotes INTEGER DEFAULT 0,
#         Downvotes INTEGER DEFAULT 0,
#         FOREIGN KEY (ErrorCode) REFERENCES AI_ERRORS(ErrorCode)
#     )
# ''')

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
    print(f"\nError found in your original 'errorease.db'!")

# 5. IF NOT FOUND IN ORIGINAL DATABASE
else:
    # First, check if it's just random text/tricks (doesn't start with 0x)
    if not error_code.lower().startswith('0x'):
        print("\nInvalid inputs, errors only!")
    else:
        # It's not in the original DB. Ask the AI!
        solution_count = 0 #count for checking database
        successful_inserts = 0 #count for insertions
        target_solutions = 3 #number of solutions to generate

        #Loop to generate multiple solutions for the same error code
        for i in range(target_solutions):
            result = create_ai_solutions(cursor, error_code) #True or False depening on successful insert
            if result:
                successful_inserts += 1

        #Counts how many solutions exist for the error code in the SOLUTIONS table
        cursor.execute("""
            SELECT COUNT(*)
            FROM SOLUTIONS
            WHERE ErrorCode = ?
        """, (error_code,))

        solution_count = cursor.fetchone()[0]

        print(f"{solution_count} solutions exist for {error_code}.")


display_error_and_solutions(cursor, error_code)


conn.commit()
conn.close()