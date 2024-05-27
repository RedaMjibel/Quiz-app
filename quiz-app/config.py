import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://reda:reda123X@52.91.135.43/quiz_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False