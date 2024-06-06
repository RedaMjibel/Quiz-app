# Flask Quiz Application

This is a web-based quiz application built using Flask. It allows users to register, login, take quizzes, view their scores, and post comments. Administrators can manage quizzes and questions.

## Features

- User registration and authentication
- Admin dashboard for managing quizzes and questions
- Taking quizzes with a time limit
- Viewing top scorers
- Posting and managing comments
- Caching with Redis for improved performance

## Prerequisites

- Python 3.x
- Redis
- A database (e.g., PostgreSQL, MySQL, SQLite)

## Setup Instructions

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/quiz-app.git
    cd quiz-app
    ```

2. **Create a Virtual Environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure the Application**:
    - Edit the `config.py` file to set your database URI and other configurations:
    ```python
    class Config:
        SECRET_KEY = 'your_secret_key'
        SQLALCHEMY_DATABASE_URI = 'your_database_uri'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        CACHE_TYPE = 'RedisCache'
        CACHE_REDIS_URL = 'redis://localhost:6379/0'
    ```

5. **Set Up the Database**:
    ```sh
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

6. **Run the Application**:
    ```sh
    flask run
    ```

7. **Access the Application**:
    Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Usage

### User Registration and Login

1. Navigate to the registration page and create an account.
2. Login using your credentials.
3. Access quizzes and view your scores.

### Admin Dashboard

1. Login as an admin user.
2. Access the admin dashboard to manage quizzes and questions.

### Taking Quizzes

1. Select a quiz from the homepage.
2. Answer the questions within the time limit.
3. Submit your answers and view your score.

### Posting Comments

1. Navigate to the contact page.
2. Fill in your name and message.
3. Submit the comment.

## Reusing the Project

For programmers who want to reuse or contribute to this project:

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/quiz-app.git
    cd quiz-app
    ```

2. **Create a Virtual Environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up the Database**:
    ```sh
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. **Run the Application**:
    ```sh
    flask run
    ```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Create a new Pull Request.
