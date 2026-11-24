import sqlite3

# Returns upvotes from solution with the given solutionID
def get_upvotes(cursor, SolutionID):
    cursor.execute("SELECT Upvotes FROM SOLUTIONS WHERE SolutionID = ?", (SolutionID,))
    result = cursor.fetchone()
    return result[0] if result else 0

# Returns downvotes from solution with the given solutionID
def get_downvotes(cursor, SolutionID):
    cursor.execute("SELECT Downvotes FROM SOLUTIONS WHERE SolutionID = ?", (SolutionID,))
    result = cursor.fetchone()
    return result[0] if result else 0

# Increments upvotes from solution with the given solutionID by 1
def increment_upvotes(cursor, SolutionID):
    cursor.execute("UPDATE SOLUTIONS SET Upvotes = Upvotes + 1 WHERE SolutionID = ?", (SolutionID,))
    cursor.connection.commit()

# Increments downvotes from solution with the given solutionID by 1
def increment_downvotes(cursor, SolutionID):
    cursor.execute("UPDATE SOLUTIONS SET Downvotes = Downvotes + 1 WHERE SolutionID = ?", (SolutionID,))
    cursor.connection.commit()

# Gets total upvotes by subtracting downvotes from upvotes
def cumulative_upvotes(cursor, SolutionID):
    cursor.execute("SELECT COALESCE(Upvotes, 0) - COALESCE(Downvotes, 0) FROM SOLUTIONS WHERE SolutionID = ?", (SolutionID,))
    result = cursor.fetchone()
    return result[0] if result else 0