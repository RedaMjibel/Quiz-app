import os
import random
import sys

# Ensure the app module can be found
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import Quiz, Question

app = create_app()
app.app_context().push()

def generate_random_question(index):
    question_text = f"Sample question {index + 1}?"
    choices = {
        "A": "Option 1",
        "B": "Option 2",
        "C": "Option 3",
        "D": "Option 4"
    }
    correct_answer = random.choice(list(choices.keys()))
    return Question(
        text=question_text,
        choices=choices,
        correct_answer=correct_answer
    )

def add_questions_to_quiz(quiz_id, num_questions=70):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        print(f"No quiz found with id {quiz_id}")
        return

    for i in range(num_questions):
        question = generate_random_question(i)
        question.quiz_id = quiz.id
        db.session.add(question)

    db.session.commit()
    print(f"Added {num_questions} random questions to quiz {quiz_id}")

if __name__ == "__main__":
    quiz_id = 1  # Change this to the id of the quiz you want to add questions to
    add_questions_to_quiz(quiz_id, 70)