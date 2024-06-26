from flask import Flask, jsonify, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail, Message
import datetime
from app import app, db
from  app import Question1


app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vinaykumar900417@gmail.com'  
app.config['MAIL_PASSWORD'] = 'fgyc cjhy lfmb fddk'  
app.config['MAIL_DEFAULT_SENDER'] = 'vinaykumar900417@gmail.com'

mail = Mail(app)
scheduler = BackgroundScheduler()



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

# Schedule email sending using BackgroundScheduler
scheduler.add_job(send_email, 'cron', hour=0, minute=0)  # Daily email at midnight
scheduler.start()

