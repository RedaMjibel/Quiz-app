from app import create_app, db
from app.models import Quiz, Question, User

app = create_app()
app.app_context().push()

def add_initial_data():
    # Add an admin user
    admin_user = User(username='elbqtouri', email='elbatouri@gmail.com', password='Erabi1991', is_admin=True)
    db.session.add(admin_user)
    
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