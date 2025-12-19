# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open in Browser
```
http://127.0.0.1:5000
```

## ✅ Test the System

1. **Register a new user:**
   - Go to: http://127.0.0.1:5000/register
   - Username: `testuser`
   - Password: `password123` (min 8 characters)
   - Click Register

2. **Login:**
   - Go to: http://127.0.0.1:5000/login
   - Enter your credentials
   - Click Login

3. **View Dashboard:**
   - After login, you'll see the dashboard
   - Check the audit logs section to see your login attempt

## 🔍 What to Observe

- **Registration**: Password is hashed before storage
- **Login**: Password is verified using bcrypt
- **Audit Logs**: Every login attempt is recorded
- **Database**: Check `database.db` - you'll see hashed passwords, not plain text

## 📊 Database Inspection

To view the database:
```bash
# Using SQLite command line
sqlite3 database.db

# Then run:
.tables
SELECT * FROM users;
SELECT * FROM audit_logs;
```

## 🎓 Key Points for Viva

1. **Hashing**: One-way conversion of password to hash
2. **Salting**: Random data added before hashing (automatic in bcrypt)
3. **Verification**: Comparing entered password hash with stored hash
4. **Audit Logging**: Recording all security events for compliance

## ⚠️ Troubleshooting

**Error: ModuleNotFoundError: No module named 'flask'**
- Solution: Run `pip install -r requirements.txt`

**Error: ModuleNotFoundError: No module named 'bcrypt'**
- Solution: Run `pip install bcrypt`

**Port already in use:**
- Solution: Change port in `app.py` (line 180): `app.run(debug=True, host='127.0.0.1', port=5001)`

---

**Ready to demonstrate!** 🎉

