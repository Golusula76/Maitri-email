from flask import Flask, jsonify, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail, Message
import pymysql
import datetime
import json

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/new_email"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vinaykumar900417@gmail.com'  
app.config['MAIL_PASSWORD'] = 'fgyc cjhy lfmb fddk'  
app.config['MAIL_DEFAULT_SENDER'] = 'vinaykumar900417@gmail.com'  

db = SQLAlchemy(app)
mail = Mail(app)
scheduler = BackgroundScheduler()

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
    print(f"{datetime.datetime.now()} - {request.method} {request.url}")

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

def send_email():
    with app.app_context():
        questions = Question1.query.all()

        
        html_content = "<html><body>"
        html_content += "<h2>Survey Results</h2>"
        
        for question in questions:
            html_content += f"<h3>{question.text}</h3>"
            html_content += "<ul>"
            html_content += f"<li>{question.option1} - Selected {question.option1_selected_count} times</li>"
            html_content += f"<li>{question.option2} - Selected {question.option2_selected_count} times</li>"
            html_content += f"<li>{question.option3} - Selected {question.option3_selected_count} times</li>"
            html_content += "</ul>"
        
        html_content += "</body></html>"

        msg = Message("Survey Results", recipients=['pradeep@maitri.nyc'])  # Replace with recipient's email
        msg.html = html_content
        mail.send(msg)
        print("Email sent!")



scheduler.add_job(send_email, 'cron', hour=15, minute=5)
scheduler.start()


if __name__ == '__main__':
    app.run(debug=True)
