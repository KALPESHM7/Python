# 📝 Mini Guestbook – Flask App

A simple **Flask** web application that lets users:
- View all submitted messages.
- Submit new messages.
- View individual messages by ID.
- Receive feedback through flash messages.

This project demonstrates:
- **GET & POST requests**
- **Routing & URL building**
- **Jinja2 template inheritance**
- **Flash messages for user feedback**
- **WSGI integration**

---

## 📌 Project Overview
The **Mini Guestbook** is built to practice Flask basics:
- `/` → Home page with a form to submit a message and view all messages.
- `/message/<int:msg_id>` → Displays a single message by its ID.
- Uses **in-memory list** for storing messages (no database required).

---

## 📂 Project Structure
```
project-folder/
│
├── app.py              # Main Flask application
├── wsgi.py             # WSGI entry point for production
├── static/
│   └── styles.css      # CSS styling
├── templates/
│   ├── base.html       # Base template with layout & navigation
│   ├── index.html      # Homepage & message form
│   └── message.html    # Single message detail page
└── README.md           # Project documentation
```

---

## 🚀 How to Run the Project

### 1️⃣ Open the Project
Open the project folder in **PyCharm** (or any Python environment).

### 2️⃣ Install Flask (if not already installed)
Run this in **Terminal** (inside PyCharm or Command Prompt):
```bash
pip install flask
```

### 3️⃣ Run the App in Development Mode
In the **Terminal**, navigate to the folder containing `app.py` and run:
```bash
set FLASK_APP=app     # Windows
export FLASK_APP=app  # macOS/Linux

set FLASK_ENV=development     # Windows
export FLASK_ENV=development  # macOS/Linux

flask run
```

**Or simply run:**
```bash
python app.py
```

### 4️⃣ Access the App
Once the server starts, open your browser and go to:
```
http://127.0.0.1:5000/
```

---

## 💡 Example Commands

Windows (CMD):
```bash
cd path\to\project-folder
set FLASK_APP=app
set FLASK_ENV=development
flask run
```

macOS / Linux (Terminal):
```bash
cd path/to/project-folder
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

---

## 📜 Features Implemented
- **GET** and **POST** routes.
- Form validation with flash messages.
- Template inheritance with Jinja2.
- URL building with `url_for`.
- Debug mode enabled for development.
- WSGI-ready via `wsgi.py`.

---

## 🛠 Notes & Assumptions
- Requires **Python 3.x** and **Flask** installed.
- Messages are **not stored in a database** (reset on server restart).
- Compatible with both Windows and macOS/Linux.

---
