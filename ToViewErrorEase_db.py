import sqlite3

conn = sqlite3.connect('errorease.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM SOLUTIONS")
rows = cursor.fetchall()

# Print
for row in rows:
    print(f"Error Code: {row[1]} | Summary: {row[2]} | Upvotes: {row[4]} | Downvotes: {row[5]}")
    print("-" * 50)

conn.close()