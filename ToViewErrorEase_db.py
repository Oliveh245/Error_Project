import sqlite3

conn = sqlite3.connect('errorease.db')
cursor = conn.cursor()

# --- ORIGINAL TABLES ---
print("\n========== ORIGINAL SOLUTIONS TABLE ==========")
cursor.execute("SELECT * FROM SOLUTIONS")
rows = cursor.fetchall()
for row in rows:
    print(f"Error Code: {row[1]} | Summary: {row[2]} | Upvotes: {row[4]} | Downvotes: {row[5]}")
    print("-" * 50)

print("\n========== ORIGINAL ERRORS TABLE ==========")
cursor.execute("SELECT * FROM ERRORS")
errors = cursor.fetchall()
for row in errors:
    print(f"Error Code: {row[0]} | Name: {row[1]} | Desc: {row[2]}")
    print("-" * 50)

#  Separate New Tables for AI writing Test
print("\n========== AI SOLUTIONS TABLE (TEST) ==========")
cursor.execute("SELECT * FROM AI_SOLUTIONS")
ai_rows = cursor.fetchall()
if ai_rows:
    for row in ai_rows:
        print(f"Error Code: {row[1]} | Summary: {row[2]} | Upvotes: {row[4]} | Downvotes: {row[5]}")
        print("-" * 50)
else:
    print("No AI solutions yet.")

print("\n========== AI ERRORS TABLE (TEST) ==========")
cursor.execute("SELECT * FROM AI_ERRORS")
ai_errors = cursor.fetchall()
if ai_errors:
    for row in ai_errors:
        print(f"Error Code: {row[0]} | Name: {row[1]} | Desc: {row[2]}")
        print("-" * 50)
else:
    print("No AI errors yet.")

conn.close()