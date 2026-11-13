import sqlite3

conn = sqlite3.connect('errorease.db')
cursor = conn.cursor()

# Ask the user for the error code
error_code = input("What is the error code? ")

# Search using a JOIN to connect the two tables together!
query = """
    SELECT ERRORS.ErrorName, ERRORS.ErrorDescription, SOLUTIONS.PlainEnglishSummary, SOLUTIONS.StepByStepFix, SOLUTIONS.Upvotes, SOLUTIONS.Downvotes
    FROM SOLUTIONS
    JOIN ERRORS ON SOLUTIONS.ErrorCode = ERRORS.ErrorCode
    WHERE SOLUTIONS.ErrorCode = ?
"""
cursor.execute(query, (error_code,))
results = cursor.fetchall()

# Check if we found anything
if results:
    # Print the main error info just once
    print(f"\n✅ Found in database!")
    print(f"Error Name: {results[0][0]}")
    print(f"Description: {results[0][1]}\n")
    print("Available Solutions:")
    print("-" * 40)

    # Loop through and print the solutions
    for row in results:
        print(f"Summary: {row[2]}")
        print(f"Fix: {row[3]}")
        print(f"Upvotes: {row[4]} | Downvotes: {row[5]}")
        print("-" * 40)
else:
    print("\n❌ No error found in database")

# Close the connection
conn.close()