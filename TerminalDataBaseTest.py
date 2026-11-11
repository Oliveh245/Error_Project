import sqlite3

conn = sqlite3.connect('errorease.db')
cursor = conn.cursor()

error_code = input("What is the error code? ")

cursor.execute("SELECT * FROM SOLUTIONS WHERE ErrorCode = ?", (error_code,))
results = cursor.fetchall()

# If found and print error details
if results:
    print("Found in database!")
    for row in results:
        print("Error Code:", row[1])
        print("Summary:", row[2])
        print("Fix:", row[3])
        print("Upvotes:", row[4])
        print("Downvotes:", row[5])
        print("-------------------")
else:
    print("No error found in database")

conn.close()