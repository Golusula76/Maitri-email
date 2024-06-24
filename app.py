import os
from flask import Flask, jsonify, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import datetime

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# Use environment variable for database URL in production
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "mysql+pymysql://root:root@localhost:3306/new_email")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define SQLAlchemy model
class Question1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option1_selected_count = db.Column(db.Integer, default=0)
    option2_selected_count = db.Column(db.Integer, default=0)
    option3_selected_count = db.Column(db.Integer, default=0)

# Middleware for logging requests
@app.before_request
def log_request_info():
    app.logger.info(f"{datetime.datetime.now()} - {request.method} {request.url}")

# Middleware for adding a custom response header
@app.after_request
def add_custom_header(response):
    response.headers['X-Custom-Header'] = 'Value'
    return response

# Error handling middleware
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500

# Routes

# Create a question
@app.route('/')
def survey_form():
    question = Question1.query.first()
    return render_template('index.html', question=question)

# Submit answer
@app.route('/submit', methods=['POST'])
def submit_answer():
    data = request.form
    question_id = int(data['question_id'])
    selected_option = int(data['answer'])

    question = Question1.query.get(question_id)
    if not question:
        abort(404, description="Question not found")

    if selected_option == 1:
        question.option1_selected_count += 1
    elif selected_option == 2:
        question.option2_selected_count += 1
    elif selected_option == 3:
        question.option3_selected_count += 1

    db.session.commit()

    return render_template('submit.html')

# Remove this for production deployment
# if __name__ == '__main__':
#     app.run(debug=True)