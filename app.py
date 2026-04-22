from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

# SQLite database connection
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    phone TEXT
)
""")
conn.commit()

# 🏠 Home Page
@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Data Redundancy System</title>
        <style>
            body {
                font-family: Arial;
                background: #f4f6f8;
                text-align: center;
                padding-top: 100px;
            }
            h1 {
                color: #333;
            }
            a {
                display: inline-block;
                margin: 15px;
                padding: 12px 20px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-size: 16px;
            }
            a:hover {
                background: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>🚀 Data Redundancy System</h1>
        <a href="/add">Add User</a>
        <a href="/view">View Details</a>
    </body>
    </html>
    """

# ➕ Add User
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        cursor.execute("SELECT * FROM details WHERE email=?", (email,))
        existing = cursor.fetchone()

        if existing:
            return "<h2 style='color:red;text-align:center;'>Duplicate entry detected!</h2><br><div style='text-align:center;'><a href='/add'>Go Back</a></div>"

        cursor.execute(
            "INSERT INTO details (name, email, phone) VALUES (?, ?, ?)",
            (name, email, phone)
        )
        conn.commit()

        return redirect("/view")

    return """
    <html>
    <head>
        <style>
            body {
                font-family: Arial;
                background: #eef2f7;
                text-align: center;
                padding-top: 50px;
            }
            form {
                background: white;
                padding: 20px;
                display: inline-block;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            input {
                margin: 10px;
                padding: 10px;
                width: 200px;
            }
            button {
                padding: 10px 20px;
                background: green;
                color: white;
                border: none;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <h2>Add User</h2>
        <form method="POST">
            <input name="name" placeholder="Name" required><br>
            <input name="email" placeholder="Email" required><br>
            <input name="phone" placeholder="Phone" required><br>
            <button type="submit">Add</button>
        </form>
    </body>
    </html>
    """

# 📋 View Data
@app.route("/view")
def view():
    cursor.execute("SELECT * FROM details")
    data = cursor.fetchall()

    rows = ""
    for row in data:
        rows += f"<tr><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"

    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial;
                background: #f8f9fa;
                text-align: center;
                padding-top: 50px;
            }}
            table {{
                margin: auto;
                border-collapse: collapse;
                width: 60%;
                background: white;
            }}
            th, td {{
                padding: 12px;
                border: 1px solid #ddd;
            }}
            th {{
                background: #007bff;
                color: white;
            }}
        </style>
    </head>
    <body>
        <h2>User Details</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
            </tr>
            {rows}
        </table>
        <br>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run()