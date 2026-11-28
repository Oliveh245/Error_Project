from flask import Flask, render_template, request, redirect, url_for
import sqlite3

from AITest import create_ai_solutions
from UpvotesDownvotes import increment_upvotes, increment_downvotes

app = Flask(__name__)

@app.route("/")
def search():
    return render_template("search.html")

# Used to keep track of solutions to make displaying details a bit easier (without refactoring)
current_solutions = []

@app.route("/search", methods=["GET", "POST"])
def handle_search():
    # Read the error code from the form (POST) OR from the URL (?code=...) (GET)
    if request.method == "POST":
        error_code = request.form.get("error_code", "").strip()
    else:
        error_code = request.args.get("code", "").strip()

    if error_code and not error_code.lower().startswith('0x'):
        if all(c in "0123456789abcdefABCDEF" for c in error_code):
            error_code = "0x" + error_code

    conn = sqlite3.connect('errorease.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute("""
        SELECT ERRORS.ErrorName, ERRORS.ErrorDescription, SOLUTIONS.PlainEnglishSummary, SOLUTIONS.StepByStepFix, SOLUTIONS.SolutionID, SOLUTIONS.Upvotes, SOLUTIONS.Downvotes
        FROM SOLUTIONS
        JOIN ERRORS ON SOLUTIONS.ErrorCode = ERRORS.ErrorCode
        WHERE SOLUTIONS.ErrorCode = ?
    """, (error_code,))
    results = cursor.fetchall()

    if not results:
        print(f"Database empty for {error_code}. Triggering AI...")
        for _ in range(3):
            create_ai_solutions(cursor, error_code)
        cursor.execute("""
            SELECT ERRORS.ErrorName, ERRORS.ErrorDescription, SOLUTIONS.PlainEnglishSummary, SOLUTIONS.StepByStepFix, SOLUTIONS.SolutionID, SOLUTIONS.Upvotes, SOLUTIONS.Downvotes
            FROM SOLUTIONS
            JOIN ERRORS ON SOLUTIONS.ErrorCode = ERRORS.ErrorCode
            WHERE SOLUTIONS.ErrorCode = ?
        """, (error_code,))
        results = cursor.fetchall()

    conn.close()

    if results:
        global current_solutions # bad practice but wcyd
        current_solutions = results
        return render_template("list.html", error_code=error_code, solutions=results)
    else:
        return render_template("no-solution.html")

@app.route("/no-solution")
def no_solution():
    return render_template("no-solution.html")

@app.route("/solutions")
def solutions():
    return render_template("list.html")

@app.route("/solution/<int:item_id>")
def solution(item_id, methods=["GET"]):
    solution = [s for s in current_solutions if s[4] == item_id][0]
    if not solution:
        return render_template("solution-empty.html")
    else:
        return render_template(
            "solution-valid.html", 
            error_code=solution[0], 
            description=solution[1], 
            solution=solution[2], 
            steps=solution[3], 
            soluton_id=solution[4], 
            upvotes=solution[5], 
            downvotes=solution[6]
        )

@app.route("/upvote/<int:solution_id>")
def upvote(solution_id):
    code = request.args.get("code", "")
    conn = sqlite3.connect('errorease.db')
    cursor = conn.cursor()
    increment_upvotes(cursor, solution_id)
    conn.close()
    return redirect(url_for("handle_search", code=code))

@app.route("/downvote/<int:solution_id>")
def downvote(solution_id):
    code = request.args.get("code", "")
    conn = sqlite3.connect('errorease.db')
    cursor = conn.cursor()
    increment_downvotes(cursor, solution_id)
    conn.close()
    return redirect(url_for("handle_search", code=code))

if __name__ == "__main__":
    app.run(debug=True)