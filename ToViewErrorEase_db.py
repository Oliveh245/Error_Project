import sqlite3

conn = sqlite3.connect('errorease.db')
cursor = conn.cursor()

#Solutions Table
print("\n========== SOLUTIONS TABLE ==========")

cursor.execute("SELECT * FROM SOLUTIONS")
rows = cursor.fetchall()

# Print
for row in rows:
    print(f"Error Code: {row[1]} | Summary: {row[2]} | Upvotes: {row[4]} | Downvotes: {row[5]}")
    print("-" * 50)

# View ERRORS
print("\n========== ERRORS TABLE ==========")

cursor.execute("SELECT * FROM ERRORS")
errors = cursor.fetchall()

for row in errors:
    print(f"Error Code: {row[0]}")
    print(f"Error Name: {row[1]}")
    print(f"Description: {row[2]}")
    print("-" * 50)

conn.close()