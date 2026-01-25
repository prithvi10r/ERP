from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/staff", methods=["GET", "POST"])
def staff_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, username, password, subject_clean FROM staff WHERE username=? AND password=?",
            (username, password)
        )

        staff = cursor.fetchone()
        conn.close()

        if staff:
            session["staff_logged_in"] = True
            session["subject"] = staff["subject_clean"]
            return redirect("/dashboard")

        return "Invalid username or password"

    return render_template("staff_login.html")


@app.route("/dashboard")
def dashboard():
    if not session.get("staff_logged_in"):
        return redirect("/staff")

    subject = session["subject"]

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Only fetch the assigned subject column
    cursor.execute(f"SELECT id, roll_no, name, department, class, {subject} FROM students")
    students = cursor.fetchall()
    conn.close()

    return render_template(
        "staff_dashboard.html",
        students=students,
        subject=subject
    )


@app.route("/update_marks", methods=["POST"])
def update_marks():
    if not session.get("staff_logged_in"):
        return redirect("/staff")

    subject = session["subject"]
    student_id = request.form["id"]
    mark = request.form["mark"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE students SET {subject}=? WHERE id=?", (mark, student_id))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        roll_no = request.form["roll_no"]

        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students WHERE roll_no=?", (roll_no,))
        student = cursor.fetchone()
        conn.close()

        if student:
            return render_template("student_view.html", student=student)

        return "Student not found"

    return render_template("student_login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/staff")


if __name__ == "__main__":
    app.run(debug=True)
