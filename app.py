"""
Secure Password Storage System using Hashing and Salting
==========================================================
This project demonstrates secure password storage using bcrypt hashing and salting,
along with security audit logging for compliance purposes.

Author: Academic Project
Subject: Security Audit and Compliance
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import bcrypt
from datetime import datetime
import os

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change this in production!

# Database file name
DATABASE = 'database.db'


def get_db_connection():
    """
    Create and return a database connection.
    This function creates the database file if it doesn't exist.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn


def init_database():
    """
    Initialize the database with required tables.
    This function creates the Users and Audit_logs tables if they don't exist.
    """
    conn = get_db_connection()
    
    # Create Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Audit_logs table for security compliance
    conn.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def validate_password(password):
    """
    Validate password strength.
    Requirements: Minimum 8 characters.
    
    Returns: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    return True, ""


def hash_password(password):
    """
    Hash a password using bcrypt with automatic salting.
    
    How it works:
    1. bcrypt automatically generates a unique salt for each password
    2. The salt is combined with the password
    3. The result is hashed using bcrypt algorithm
    4. The hash includes the salt, so we don't need to store it separately
    
    Returns: Hashed password (as bytes, converted to string for storage)
    """
    # Generate salt and hash password in one step
    # bcrypt.hashpw() automatically generates a unique salt
    salt = bcrypt.gensalt()  # Generate a random salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hash password with salt
    return hashed.decode('utf-8')  # Convert bytes to string for database storage


def verify_password(password, password_hash):
    """
    Verify a password against a stored hash.
    
    How it works:
    1. bcrypt extracts the salt from the stored hash
    2. Uses the same salt to hash the provided password
    3. Compares the new hash with the stored hash
    4. Returns True if they match, False otherwise
    
    Returns: True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def log_audit_event(username, status):
    """
    Log security events for audit and compliance purposes.
    
    This function records every login attempt (success or failure) with:
    - Username attempted
    - Status (success/failure)
    - Timestamp
    
    This is essential for security audits and compliance requirements.
    """
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO audit_logs (username, status, timestamp) VALUES (?, ?, ?)',
        (username, status, datetime.now())
    )
    conn.commit()
    conn.close()


@app.route('/')
def index():
    """Home page - redirects to login"""
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    User Registration Module
    
    Security Features:
    1. Validates password strength (min 8 characters)
    2. Hashes password using bcrypt (automatic salting)
    3. Stores ONLY hashed password, never plain text
    4. Prevents duplicate usernames
    """
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        # Validate input
        if not username or not password:
            flash('Username and password are required!', 'error')
            return render_template('register.html')
        
        # Validate password strength
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            flash(error_msg, 'error')
            return render_template('register.html')
        
        # Hash the password before storing
        # IMPORTANT: We NEVER store plain text passwords
        password_hash = hash_password(password)
        
        # Store user in database
        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists! Please choose another.', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User Login Module
    
    Security Features:
    1. Verifies password using bcrypt
    2. Logs every login attempt (success or failure) for audit
    3. Prevents timing attacks by always checking password (even if user doesn't exist)
    """
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        if not username or not password:
            flash('Username and password are required!', 'error')
            return render_template('login.html')
        
        # Get user from database
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()
        conn.close()
        
        # Verify password
        if user and verify_password(password, user['password_hash']):
            # Login successful
            session['username'] = username
            log_audit_event(username, 'success')  # Log successful login
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Login failed
            log_audit_event(username, 'failure')  # Log failed login attempt
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    """
    User Dashboard
    
    Displays:
    - Welcome message
    - Recent audit logs (for demonstration)
    - Security information
    """
    if 'username' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    # Get recent audit logs for display
    conn = get_db_connection()
    recent_logs = conn.execute(
        'SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 10'
    ).fetchall()
    conn.close()
    
    return render_template('dashboard.html', 
                         username=session['username'],
                         audit_logs=recent_logs)


@app.route('/logout')
def logout():
    """Logout user and clear session"""
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    # Initialize database on first run
    init_database()
    
    # Run the Flask application
    print("\n" + "="*50)
    print("Secure Password Storage System")
    print("="*50)
    print("\nStarting server...")
    print("Open your browser and go to: http://127.0.0.1:5000")
    print("\nPress CTRL+C to stop the server")
    print("="*50 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)

