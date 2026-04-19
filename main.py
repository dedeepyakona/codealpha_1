from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="KonaDedeepy@16",
    database="codeaplha_db"
)

cursor = conn.cursor()

@app.route("/")
def home():
    return "<h1>Data Redundancy System</h1><a href='/add'>Add User</a> | <a href='/view'>View details</a>"

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        cursor.execute("INSERT INTO details (name, email, phone) VALUES (%s, %s, %s)",
                       (name, email, phone))
        conn.commit()

        return redirect("/view")

    return '''
    <form method="POST">
        Name: <input name="name"><br>
        Email: <input name="email"><br>
        Phone: <input name="phone"><br>
        <button type="submit">Add</button>
    </form>
    '''

@app.route("/view")
def view():
    cursor.execute("SELECT * FROM details")
    data = cursor.fetchall()
    return "<br>".join([str(row) for row in data])

if __name__ == "__main__":
    app.run(debug=True)
    