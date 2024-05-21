from app import create_app, db
from app.models import Quiz, Question

app = create_app()
app.app_context().push()

def add_initial_data():
    quiz = Quiz(title='Sample Quiz')
    db.session.add(quiz)
    questions = [
        Question(text='What is 2 + 2?', choices={'A': '3', 'B': '4', 'C': '5'}, correct_answer='B', quiz=quiz),
        Question(text='What is the capital of France?', choices={'A': 'Paris', 'B': 'London', 'C': 'Berlin'}, correct_answer='A', quiz=quiz),
    ]
    db.session.add_all(questions)
    db.session.commit()
    print('Initial data added.')

if __name__ == '__main__':
    add_initial_data()