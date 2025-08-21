import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    # If you keep username `postgres` and password `Kalpesh@01`, URI must encode '@' as %40
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:Kalpesh%4001@localhost/publishable_notes"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
