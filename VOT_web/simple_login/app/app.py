from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure to use a secure, unique key

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)", (email, password_hash))
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            # Output the specific MySQL error to help identify the issue
            flash(f"Database error: {err}", "danger")
            print("Database error:", err)  # Log this in the Docker output
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user[0], password):
                flash("Login successful!", "success")
                return redirect(url_for('main'))
            else:
                flash("Invalid credentials. Please try again.", "danger")
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "danger")
            print("Database error:", err)
        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')


@app.route('/main')
def main():
    if 'user_id' in session:
        return render_template('main.html', email=session['email'])
    else:
        flash("Please log in to access this page", "warning")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    app.run(host='0.0.0.0', port=5000)
