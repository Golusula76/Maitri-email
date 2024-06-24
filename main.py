from app import app, db  # Import your Flask app instance and SQLAlchemy db object

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)