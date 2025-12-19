# Secure Password Storage System using Hashing and Salting

## 📋 Project Overview

This is a complete mini project demonstrating secure password storage using **bcrypt hashing and salting** with security audit logging for compliance purposes. The project is designed for undergraduate students studying **Security Audit and Compliance**.

## 🎯 Learning Objectives

- Understand password hashing and salting concepts
- Implement secure password storage practices
- Learn about security audit logging
- Understand compliance requirements for password protection

## 🔧 Technology Stack

- **Python 3.x** - Programming language
- **Flask** - Web framework
- **SQLite** - Database
- **bcrypt** - Password hashing library
- **HTML/CSS** - Frontend

## 📁 Project Structure

```
secure-password-storage/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── database.db           # SQLite database (created automatically)
├── README.md             # This file
│
├── templates/            # HTML templates
│   ├── register.html     # User registration page
│   ├── login.html        # User login page
│   └── dashboard.html    # User dashboard
│
└── static/              # Static files
    └── style.css        # CSS stylesheet
```

## 🚀 Installation & Setup

### Step 1: Install Python
Make sure you have Python 3.7 or higher installed on your system.

### Step 2: Install Dependencies
Open terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- bcrypt (password hashing library)

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access the Application
Open your web browser and go to:
```
http://127.0.0.1:5000
```

## 📖 How to Use

1. **Register a New User**
   - Click on "Register here" or go to `/register`
   - Enter a username and password (minimum 8 characters)
   - Click "Register"
   - Your password will be hashed and stored securely

2. **Login**
   - Go to `/login`
   - Enter your username and password
   - Click "Login"
   - Your login attempt will be logged in the audit trail

3. **View Dashboard**
   - After successful login, you'll see the dashboard
   - View recent audit logs
   - Learn about security features

## 🔐 Security Features Explained

### 1. Password Hashing
- **What it is**: Converting a password into a fixed-length string using a mathematical function
- **Why it's important**: Even if someone accesses the database, they cannot see your actual password
- **How it works**: bcrypt uses a one-way hash function that cannot be reversed

### 2. Salting
- **What it is**: Adding random data to a password before hashing
- **Why it's important**: Prevents rainbow table attacks and ensures unique hashes even for identical passwords
- **How it works**: bcrypt automatically generates a unique salt for each password

### 3. Password Verification
- **What it is**: Checking if an entered password matches the stored hash
- **How it works**: bcrypt extracts the salt from the stored hash, applies it to the entered password, and compares the results

### 4. Audit Logging
- **What it is**: Recording all security events (login attempts)
- **Why it's important**: Required for security compliance and helps detect unauthorized access
- **What's logged**: Username, status (success/failure), and timestamp

## 🗄️ Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| username | TEXT | Unique username |
| password_hash | TEXT | Hashed password (NOT plain text) |
| created_at | TIMESTAMP | Account creation time |

### Audit_logs Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| username | TEXT | Username that attempted login |
| status | TEXT | 'success' or 'failure' |
| timestamp | TIMESTAMP | Time of login attempt |

## 📝 Code Explanation

### Key Functions

1. **`hash_password(password)`**
   - Generates a salt and hashes the password
   - Returns the hashed password as a string

2. **`verify_password(password, password_hash)`**
   - Verifies if the entered password matches the stored hash
   - Returns True if match, False otherwise

3. **`log_audit_event(username, status)`**
   - Records login attempts in the audit_logs table
   - Essential for security compliance

4. **`validate_password(password)`**
   - Checks if password meets minimum requirements (8 characters)
   - Returns validation result and error message

## 🎓 Viva Questions & Answers

### Q1: What is password hashing?
**Answer**: Password hashing is the process of converting a password into a fixed-length string using a mathematical function. It's a one-way process, meaning you cannot reverse the hash to get the original password. This ensures that even if someone accesses the database, they cannot see actual passwords.

### Q2: What is salting and why is it important?
**Answer**: Salting is adding random data to a password before hashing. Each password gets a unique salt, so even if two users have the same password, their hashes will be different. This prevents rainbow table attacks where attackers use pre-computed hash tables to crack passwords.

### Q3: How does bcrypt work?
**Answer**: bcrypt automatically generates a unique salt for each password and combines it with the password before hashing. The salt is included in the final hash, so we don't need to store it separately. During verification, bcrypt extracts the salt from the stored hash and uses it to verify the entered password.

### Q4: Why do we need audit logging?
**Answer**: Audit logging is required for security compliance. It helps:
- Track all login attempts (successful and failed)
- Detect unauthorized access attempts
- Maintain a security audit trail
- Meet compliance requirements for security audits

### Q5: What security best practices are implemented?
**Answer**:
1. **Never store plain text passwords** - Only hashed passwords are stored
2. **Use strong hashing algorithm** - bcrypt is industry-standard
3. **Automatic salting** - Each password gets unique salt
4. **Password strength validation** - Minimum 8 characters required
5. **Audit trail** - All login attempts are logged
6. **Session management** - Secure session handling

### Q6: What happens if someone accesses the database?
**Answer**: Even if someone accesses the database, they cannot get actual passwords because:
- Only hashed passwords are stored (not plain text)
- Hashing is a one-way function (cannot be reversed)
- Each password has a unique salt, making it extremely difficult to crack
- bcrypt is computationally expensive, making brute-force attacks impractical

## 🔍 Testing the System

1. **Test Registration**
   - Try registering with a password less than 8 characters (should fail)
   - Register with a valid password (should succeed)
   - Try registering the same username twice (should fail)

2. **Test Login**
   - Try logging in with wrong password (should fail and be logged)
   - Login with correct password (should succeed and be logged)
   - Check dashboard to see audit logs

3. **Test Audit Logging**
   - Make multiple login attempts (both success and failure)
   - Check the dashboard to see all attempts logged with timestamps

## ⚠️ Important Notes

- This is a **prototype/educational project** for learning purposes
- For production use, additional security measures are needed:
  - HTTPS encryption
  - Rate limiting for login attempts
  - Password complexity requirements
  - Account lockout after failed attempts
  - Secure session management
  - Environment variables for secrets

## 📚 References

- Flask Documentation: https://flask.palletsprojects.com/
- bcrypt Documentation: https://github.com/pyca/bcrypt/
- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/

## 👨‍💻 Project Features Summary

✅ User registration with password validation  
✅ Secure password hashing using bcrypt  
✅ Automatic password salting  
✅ User login with password verification  
✅ Security audit logging  
✅ Dashboard with audit trail display  
✅ Clean and simple user interface  
✅ Well-commented code for learning  
✅ Viva-ready explanations  

## 🎯 Conclusion

This project demonstrates fundamental security concepts:
- **Hashing**: One-way password encryption
- **Salting**: Random data addition for uniqueness
- **Audit Logging**: Security event tracking
- **Compliance**: Meeting security audit requirements

---

**Project Created For**: Security Audit and Compliance Course  
**Academic Purpose**: Educational demonstration of secure password storage
#   S e c u r e - P a s s w o r d - S t o r a g e - S y s t e m - u s i n g - H a s h i n g - a n d - S a l t i n g -  
 