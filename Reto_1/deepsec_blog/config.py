import os
import base64

class Config:
    SECRET_KEY = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    REMEMBER_COOKIE_HTTPONLY = False
