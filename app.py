from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
import config

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Config
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB


mysql = MySQL(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm = request.form['confirmPassword']

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
            mysql.connection.commit()
            flash("Registration successful. Please login.", "success")
            return redirect(url_for('login'))  # Create this route later
        except Exception as e:
            flash(f"Registration failed: {e}", "danger")
            return redirect(url_for('register'))
        finally:
            cur.close()

    return render_template('register.html')  # or 'templates/register.html' depending on setup

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')

        if not email or not password:
            flash("Email and password are required.", "danger")
            return redirect(url_for('login'))

        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT id, name, password FROM users WHERE email = %s", (email,))
            user = cur.fetchone()

            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                flash("Login successful.", "success")
                return redirect(url_for('home'))  # update with your actual home/dashboard route
            else:
                flash("Invalid email or password.", "danger")
                return redirect(url_for('login'))
        except Exception as e:
            flash(f"Login failed: {e}", "danger")
            return redirect(url_for('login'))
        finally:
            cur.close()

    return render_template('login.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    full_name = request.form.get('fullName')
    email = request.form.get('email')
    phone = request.form.get('phone')
    subject = request.form.get('subject')
    message = request.form.get('message')

    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO contact_messages (full_name, email, phone, subject, message)
            VALUES (%s, %s, %s, %s, %s)
        """, (full_name, email, phone, subject, message))
        mysql.connection.commit()
        flash("Message sent successfully.", "success")
    except Exception as e:
        flash(f"Failed to send message: {e}", "danger")
    finally:
        cur.close()
        
    return redirect(url_for('contact'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        flash("Please log in to continue.", "warning")
        return redirect(url_for('login'))

    user_name = session.get('user_name', 'Guest')
    return render_template('home.html', user_name=user_name)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/cost_estimator')
def cost_estimator():
    return render_template('cost_estimator.html')

@app.route('/portofolio')
def portofolio():
    return render_template('portofolio.html')

if __name__ == '__main__':
    app.run(debug=True)