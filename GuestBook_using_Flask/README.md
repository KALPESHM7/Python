# Mini Guestbook

## 📌 Project Overview
The **Mini Guestbook** is a simple web application built using Flask.  
Users can submit and view messages in a guestbook-style interface.  
This project demonstrates basic Flask concepts such as:
- Project structure
- Routing & URL building
- GET and POST request handling
- Flash messages
- Development server & debugging
- WSGI integration

---

## 📂 Project Structure
```
flask-guestbook/
  ├─ app.py
  ├─ wsgi.py
  ├─ templates/
  │   ├─ base.html
  │   ├─ index.html
  │   └─ message.html
  ├─ static/
  │   └─ styles.css
  └─ requirements.txt
```

---

## ⚙️ Setup Instructions

### 1️⃣ Install Dependencies
Make sure Python is installed. Then run:
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Application (Windows/macOS/Linux)
```bash
flask --app app --debug run
```

---

## 🚀 Usage
- Open your browser and go to: `http://127.0.0.1:5000/`
- Submit a message using the form.
- View all messages on the home page.
- Click a message to view its details.

---

## 📝 Notes & Assumptions
- Messages are stored **in-memory** (will reset when the server restarts).
- Designed for educational/demo purposes.
- Can run in any Python environment with Flask installed (no virtual environment required).

---

## 📦 Requirements
```
Flask>=3.0
```
