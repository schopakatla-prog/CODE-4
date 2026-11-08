from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database with a expanded vendor schema
def init_db():
    conn = sqlite3.connect('vendors.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT NOT NULL,
            sector TEXT NOT NULL,
            services TEXT NOT NULL,
            experience INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Helper function to get database connection with dictionary rows
def get_db_connection():
    conn = sqlite3.connect('vendors.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    vendors = conn.execute("SELECT * FROM vendors").fetchall()
    conn.close()
    return render_template("index.html", vendors=vendors)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        company = request.form.get("company")
        sector = request.form.get("sector")
        services = request.form.get("services")
        experience = request.form.get("experience")
        email = request.form.get("email")

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO vendors (name, company, sector, services, experience, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, company, sector, services, experience, email))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template("register.html")

@app.route("/profile/<int:vendor_id>")
def profile(vendor_id):
    conn = get_db_connection()
    vendor = conn.execute("SELECT * FROM vendors WHERE id = ?", (vendor_id,)).fetchone()
    conn.close()
    
    if vendor is None:
        return "Vendor profile not found", 404
        
    return render_template("profile.html", vendor=vendor)

if __name__ == "__main__":
    app.run(debug=True)