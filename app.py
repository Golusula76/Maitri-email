from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask import Flask, jsonify, request, render_template, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


    
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/new_Email2"  # Adjust this to your database URI
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

# Routes

# Create a question
@app.route('/')
def survey_form():
    question = Question1.query.first()  # Assuming you want to fetch the first question for simplicity
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


