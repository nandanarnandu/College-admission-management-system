from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("1.html")

@app.route("/home", methods=["POST"])
def login():
    name = request.form.get("name")
    password = request.form.get("password")
    if name == "student" and password == "student":
        return render_template("2.html")
    elif name == "admin" and password == "admin":
        return render_template("2a.html")
    else:
        return render_template("11.html")


@app.route("/signout")
def signout():
    return render_template("1.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register")
def register():
    return render_template("r1.html")


@app.route("/student")
def student():
    return render_template("2.html")

@app.route("/reg", methods=["POST"])
def reg():
    # Retrieve form data
    name = request.form.get("name")
    father = request.form.get("father")
    number = request.form.get("num")
    email = request.form.get("email")
    rank = request.form.get("rank")
    telephone = request.form.get("telephone")  # Fixed indentation

    # Check that all required fields have values
    if not all([name, father, number, email, rank, telephone]):
        return render_template("r1.html")  # Return to form page if validation fails

    with sql.connect("database.db") as con:
        cur = con.cursor()
        
        # Insert new record into the database
        cur.execute(
            "INSERT INTO STUDENTS (name, father, num, email, rank, telephone) VALUES (?, ?, ?, ?, ?, ?)",
            (name, father, number, email, rank, telephone)
        )
        con.commit()  # Commit the transaction
        return render_template("success.html")
    

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM STUDENTS")
    rows = cur.fetchall()
    return render_template("list.html", rows=rows)

@app.route('/list2')
def list2():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM STUDENTS")
    rows = cur.fetchall()
    return render_template("list2.html", rows=rows)

@app.route("/back")
def back():
    return render_template("2.html")


@app.route("/already")
def already():
    return render_template("alread.html")

@app.route("/see", methods=['POST'])
def see():
    phone = request.form.get("num")
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM STUDENTS WHERE num=?", (phone,))
    k = cur.fetchall()

    if k:
        return render_template("list.html", rows=k)
    else:
        return render_template("not.html")

@app.route("/admin")
def admin():
    return render_template("2a.html")

@app.route("/cutoff")
def cutoff():
    return render_template("cutoff.html")

@app.route("/see2", methods=['POST'])
def see2():
    name = request.form.get("name")
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM STUDENTS WHERE name=?", (name,))
    k = cur.fetchall()
    return render_template("list2.html", rows=k)

@app.route("/reset_table")
def reset_table():
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            print("Connected to the database.")
            
            # Drop the STUDENTS table if it exists
            cur.execute("DROP TABLE IF EXISTS STUDENTS;")
            print("Dropped STUDENTS table if it existed.")

            # Re-create the STUDENTS table
            cur.execute('''CREATE TABLE STUDENTS (
                            name TEXT,
                            father TEXT,
                            num TEXT,
                            email TEXT,
                            rank TEXT,
                            telephone TEXT,
                            dorm TEXT)''')
            con.commit()
            print("Re-created STUDENTS table.")
        return "Table reset successfully, and all data has been cleared."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)
