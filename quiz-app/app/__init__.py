from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    from app import routes, models
    from app.models import Quiz, Question  # Import models here
    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all()
        # Add initial data if not exists
        if not Quiz.query.first():
            quiz = Quiz(title='Sample Quiz')
            db.session.add(quiz)
            question1 = Question(text='What is 2 + 2?', choices={'A': '3', 'B': '4', 'C': '5'}, correct_answer='B', quiz=quiz)
            question2 = Question(text='What is the capital of France?', choices={'A': 'Paris', 'B': 'London', 'C': 'Berlin'}, correct_answer='A', quiz=quiz)
            db.session.add(question1)
            db.session.add(question2)
            db.session.commit()

    return app