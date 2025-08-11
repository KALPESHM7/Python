# this file is used by WSGI servers to run the app in production
from app import app

if __name__=="__main__":
    app.run()