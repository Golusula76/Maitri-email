from flask import Flask, jsonify, request, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)

# Adjust this to your PostgreSQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.cvwogapzopwlimzonxxq:ajaxeNirQzM8JVJ7@aws-0-ap-south-1.pooler.supabase.com:6543/postgres'
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

# Create the database and table if they don't exist
with app.app_context():
    db.create_all()

# Routes

# Survey form
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

# Ensure the app is run when this script is executed directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
