# Publishable Notes

A Flask-based web application for creating, managing, and publishing notes with user authentication.

## Features
- User Registration and Login (Flask-Login, Flask-WTF)
- PostgreSQL Database for persistence (SQLAlchemy ORM)
- Create, update, delete personal notes
- Archive notes for later use
- Public posts page
- Tagging system for notes
- Admin user seeded by default (`admin@example.com` / `admin`)

## Technologies Used
- **Flask** (Backend framework)
- **Flask-Login** (Authentication)
- **Flask-WTF** (Forms & Validation)
- **PostgreSQL** (Database)
- **SQLAlchemy** (ORM)
- **Jinja2** (Templating)
- **HTML, CSS** (Frontend)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KALPESHM7/Python.git
   cd Python/Publishable_notes
   ```

2. Create a virtual environment & activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate    # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the PostgreSQL database in `config.py`. Example:
   ```python
   SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost/publishable_notes"
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application:
   ```bash
   python app.py
   ```

7. Access the app at:
   ```
   http://127.0.0.1:5000
   ```

## Default Admin Login
```
Email: admin@example.com
Password: admin
```

## Project Structure
```
Publishable_notes/
│── app.py
│── config.py
│── models.py
│── forms.py
│── requirements.txt
│── routes/
│   ├── auth.py
│   ├── notes.py
│   ├── posts.py
│   └── tags.py
│── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── notes.html
│   └── posts.html
│── static/
│   └── style.css
```

## GitHub Repository
🔗 [Publishable Notes on GitHub](https://github.com/KALPESHM7/Python/tree/main/Publishable_notes)

---
Made with ❤️ using Flask and PostgreSQL.
