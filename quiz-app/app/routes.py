from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, session
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User, Quiz, Question, QuizResult
from app.forms import RegistrationForm, LoginForm, QuestionForm
from app.decorators import admin_required
import random


bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('Username or email already exists. Please choose a different one.', 'danger')
        else:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('main.login'))
    else:
        if request.method == 'POST':
            flash('Registration unsuccessful. Please check your inputs.', 'danger')
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    else:
        if request.method == 'POST':
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions
    num_questions = min(len(questions), 10)  # Adjust number of questions to sample
    selected_questions = random.sample(questions, num_questions)  # Select random questions
    if request.method == 'POST':
        score = 0
        for question in selected_questions:
            user_answer = request.form.get(str(question.id))
            if user_answer == question.correct_answer:
                score += 1
        result = QuizResult(score=score, user_id=current_user.id, quiz_id=quiz.id)
        db.session.add(result)
        db.session.commit()
        if score == 0:
            flash(f'You scored {score} out of {num_questions}', 'danger')
        else:
            flash(f'You scored {score} out of {num_questions}', 'success')
        return redirect(url_for('main.index'))
    return render_template('quiz.html', quiz=quiz, questions=selected_questions)

@bp.route('/admin')
@login_required
@admin_required
def admin():
    quizzes = Quiz.query.all()
    users = User.query.all()
    return render_template('admin.html', quizzes=quizzes, users=users)

@bp.route('/admin/add_question/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_question(quiz_id):
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(
            text=form.text.data,
            choices={
                "A": form.choice_a.data,
                "B": form.choice_b.data,
                "C": form.choice_c.data,
                "D": form.choice_d.data
            },
            correct_answer=form.correct_answer.data,
            quiz_id=quiz_id
        )
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully!', 'success')
        return redirect(url_for('main.admin'))
    return render_template('add_question.html', form=form, quiz_id=quiz_id)

@bp.route('/admin/delete_question/<int:question_id>', methods=['POST'])
@login_required
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!', 'success')
    return redirect(url_for('main.admin'))

@bp.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'], endpoint='quiz_view')
@login_required
def quiz_view(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Check if the quiz start time is set in the session
    if 'quiz_start_time' not in session:
        session['quiz_start_time'] = datetime.utcnow()
    
    # Calculate the elapsed time
    quiz_start_time = session['quiz_start_time']
    time_elapsed = datetime.utcnow() - quiz_start_time
    
    # If the time limit is exceeded, redirect to a timeout page or result page
    if time_elapsed > timedelta(minutes=1):
        flash('Time is up!', 'danger')
        return redirect(url_for('main.quiz_timeout', quiz_id=quiz.id))
    
    questions = quiz.questions
    num_questions = min(len(questions), 10)
    selected_questions = random.sample(questions, num_questions)
    
    if request.method == 'POST':
        score = 0
        for question in selected_questions:
            user_answer = request.form.get(str(question.id))
            if user_answer == question.correct_answer:
                score += 1
        result = QuizResult(score=score, user_id=current_user.id, quiz_id=quiz.id)
        db.session.add(result)
        db.session.commit()
        flash(f'You scored {score} out of {num_questions}', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('quiz.html', quiz=quiz, questions=selected_questions)

@bp.route('/quiz_timeout/<int:quiz_id>', methods=['GET'])
@login_required
def quiz_timeout(quiz_id):
    return render_template('quiz_timeout.html', quiz_id=quiz_id)