🔐 Secure Password Storage System using Hashing and Salting

A secure and compliance-oriented mini project that demonstrates industry-standard password storage techniques using bcrypt hashing and automatic salting, along with security audit logging.
This project is developed for academic purposes under the Security Audit and Compliance domain.

📌 Project Description

Insecure password storage is one of the leading causes of data breaches.
This project focuses on implementing a secure authentication system where passwords are never stored in plain text. Instead, strong cryptographic hashing and salting techniques are used to ensure confidentiality and integrity.

Additionally, the system maintains audit logs for all authentication attempts, fulfilling basic security audit and compliance requirements.

🎯 Objectives

Implement secure password storage using bcrypt

Understand hashing and salting mechanisms

Prevent rainbow table and brute-force attacks

Maintain audit logs for login attempts

Demonstrate security compliance concepts in practice

🛠️ Technology Stack

Python 3.x

Flask

SQLite

bcrypt

HTML & CSS

📁 Project Structure
secure-password-storage/
│
├── app.py
├── requirements.txt
├── database.db
├── README.md
│
├── templates/
│   ├── register.html
│   ├── login.html
│   └── dashboard.html
│
└── static/
    └── style.css

🚀 Installation & Setup
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Run the Application
python app.py

3️⃣ Open in Browser
http://127.0.0.1:5000

🔐 Security Features
✔ Password Hashing

Uses bcrypt, a strong adaptive hashing algorithm

Hashing is one-way and irreversible

✔ Automatic Salting

bcrypt automatically generates a unique salt for each password

Prevents rainbow table attacks

✔ Secure Authentication

Password verification without exposing original credentials

Safe comparison of hashed values

✔ Audit Logging

Logs all login attempts (success & failure)

Records username, status, and timestamp

Supports security audit and compliance requirements

🗄️ Database Schema
Users Table
Field	Description
id	Primary Key
username	Unique username
password_hash	bcrypt hashed password
created_at	Account creation time
Audit Logs Table
Field	Description
id	Primary Key
username	Login attempt user
status	success / failure
timestamp	Login attempt time
🧪 Testing Scenarios

Weak password rejection

Duplicate username prevention

Failed login detection

Successful authentication

Audit log verification

⚠️ Limitations

HTTPS not implemented (development only)

No account lockout mechanism

Rate limiting not applied

Not production-ready

🔮 Future Enhancements

HTTPS & SSL encryption

Account lockout after failed attempts

Password complexity rules

Role-based access control

Cloud deployment

🎓 Academic Relevance

This project is suitable for:

Security Audit & Compliance

Information Security

Cyber Security Fundamentals

Secure Software Development

📌 Conclusion

This project demonstrates a secure, audit-compliant authentication system using modern cryptographic techniques.
It effectively bridges theoretical security concepts with practical implementation, making it ideal for academic evaluation and viva examinations.

📚 References

Flask Documentation

bcrypt Documentation

OWASP Password Storage Cheat Sheet

