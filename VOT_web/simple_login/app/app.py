from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure to use a secure, unique key
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
            cursor.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user[1], password):
                # Set session variable to indicate the user is logged in
                session['user_id'] = user[0]
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
    if 'user_id' not in session:
        flash("Please log in to access the gallery", "warning")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT filename FROM images ORDER BY uploaded_at DESC")
    images = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('main.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        flash("Please log in to upload images", "warning")
        return redirect(url_for('login'))

    if 'file' not in request.files or request.files['file'].filename == '':
        flash("No file selected", "warning")
        return redirect(url_for('main'))

    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Save image data to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO images (user_id, filename) VALUES (%s, %s)",
        (session['user_id'], filename)
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash("Image uploaded successfully!", "success")
    return redirect(url_for('main'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    app.run(host='0.0.0.0', port=5000)
