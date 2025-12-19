🔐 Secure Password Storage System using Advanced Hashing & Salting
With Audit Logging and Compliance-Oriented Design
📌 Project Abstract

In today’s digital era, improper password storage is one of the major causes of data breaches.
This project, Secure Password Storage System using Hashing and Salting, is designed to demonstrate industry-standard password security practices using bcrypt, along with security audit logging to meet compliance and audit requirements.

The system ensures that user passwords are never stored in plain text, protects against brute-force and rainbow table attacks, and maintains a complete audit trail of authentication activities.
This project is especially suitable for students studying Security Audit, Information Security, and Compliance Frameworks.

🎯 Project Objectives

To implement secure password storage using strong cryptographic hashing

To demonstrate automatic salting for enhanced security

To record and maintain audit logs for authentication events

To understand security compliance requirements in authentication systems

To build a real-world applicable security model for web applications

🛠️ Technology Stack
Component	Technology
Programming Language	Python 3.x
Backend Framework	Flask
Database	SQLite
Password Security	bcrypt
Frontend	HTML, CSS
Security Concept	Hashing, Salting, Audit Logging
📁 Project Architecture & Structure
secure-password-storage/
│
├── app.py                 # Core Flask application & security logic
├── requirements.txt       # Required Python libraries
├── database.db            # SQLite database (auto-generated)
├── README.md              # Project documentation
│
├── templates/
│   ├── register.html      # Secure user registration interface
│   ├── login.html         # Authentication page
│   └── dashboard.html     # Dashboard with audit trail
│
└── static/
    └── style.css          # UI styling

🚀 Installation & Execution Steps
Step 1: Prerequisites

Python 3.7 or above

Basic knowledge of Flask

Step 2: Install Dependencies
pip install -r requirements.txt

Step 3: Run the Application
python app.py

Step 4: Access via Browser
http://127.0.0.1:5000

🔐 Core Security Concepts Implemented
1️⃣ Password Hashing

Passwords are converted into irreversible cryptographic hashes

bcrypt uses adaptive hashing, making brute-force attacks computationally expensive

Even database administrators cannot view actual passwords

2️⃣ Automatic Salting

A unique random salt is generated for every password

Prevents:

Rainbow table attacks

Hash collision attacks

bcrypt internally manages salt storage securely

3️⃣ Secure Password Verification

User-entered password is hashed using the same salt

Hashes are compared without exposing original passwords

Ensures secure authentication flow

4️⃣ Audit Logging (Compliance Feature)

Every login attempt is logged with:

Username

Login status (Success / Failure)

Timestamp

Essential for:

Security audits

Intrusion detection

Compliance verification

🗄️ Database Design (Normalized & Secure)
🔹 Users Table
Field	Description
id	Unique user identifier
username	Unique login name
password_hash	bcrypt hashed password
created_at	Account creation timestamp
🔹 Audit Logs Table
Field	Description
id	Unique log identifier
username	Login attempt user
status	success / failure
timestamp	Login attempt time
🧠 Key Functional Modules
🔹 hash_password(password)

Generates salt + hash using bcrypt

Returns secure hash

🔹 verify_password(password, stored_hash)

Verifies password without revealing hash

Returns authentication result

🔹 log_audit_event(username, status)

Records authentication activity

Supports security compliance

🔹 validate_password(password)

Enforces password policy (minimum length)

Prevents weak credentials

🧪 Testing & Validation

✔ Weak password rejection
✔ Duplicate username prevention
✔ Successful & failed login detection
✔ Audit trail verification
✔ Secure password comparison
