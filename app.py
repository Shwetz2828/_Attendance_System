import os  # Module for interacting with the operating system
from flask import Flask, render_template, redirect, url_for, request # Flask web framework and related utilities
from flask_sqlalchemy import SQLAlchemy # Flask extension for SQLAlchemy ORM
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user # Flask extension for user authentication
from flask_wtf import FlaskForm # Flask extension for handling web forms
from wtforms import StringField, PasswordField, SubmitField  # Classes  for form fields
from wtforms.validators import InputRequired, Length, ValidationError # Validators for form fields
from flask_bcrypt import Bcrypt # Flask extension for hashing passwords
import secrets # Module for generating cryptographically strong random numbers
import face_recognition # Library for face recognition tasks
import cv2 # OpenCV library for computer vision tasks
import csv # Module for reading and writing CSV files
from datetime import datetime # Module for working with dates and times
import mysql.connector # Connector for MySQL database
import pyttsx3 # Library for text-to-speech conversion
import time # Module for time-related functions

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = secrets.token_hex(16)

# MySQL database configuration
DATABASE_CONFIG = {
    'host': '127.0.0.1',
    'port': 3307,
    'database': 'major',
    'username': 'root',
    'password': 'root123'
}

# MySQL connection string
mysql_uri = f"mysql+mysqlconnector://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

# Registration form
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

# Login form
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/record-attendance')
def record_attendance():
    print("Attendance recording initiated.")


     # This includes the face recognition and attendance marking process
    import face_recognition  # Library for facial recognition tasks
    import cv2  # OpenCV library for computer vision tasks
    import numpy as np  # NumPy library for numerical operations, often used with OpenCV
    import csv  # Module for reading and writing CSV files
    from datetime import datetime  # Module for working with dates and times
    import mysql.connector  # Connector for MySQL database
    import pyttsx3  # Library for text-to-speech conversion
    import time  # Module for time-related functions


 
    engine = pyttsx3.init()

    def announce(text):
        engine.say(text)
        engine.runAndWait()

    # Load known face encodings and their names
    known_faces = {
        "jobs": "photos/jobs.jpg",
        "cheran": "photos/cheran.jpg",
        "shwetha":"photos/shweta.jpg",
        "chinmay":"photos/chinmay.jpg",
        "naveen": "photos/naveen.jpg"  
    }

    known_face_encodings = []
    known_faces_names = []

    for name, image_path in known_faces.items():
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_faces_names.append(name)

    # Connect to MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        port="3307",
        user="root",
        password="root123",
        database="major"
    )

    # Initialize cursor
    mycursor = mydb.cursor()

    # Create CSV file for attendance
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    csv_filename = f'{current_date}.csv'

    # Set up video capture
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open video capture device")
        exit()

    for name in known_faces_names:
        recognized = False
        attempts = 0  # Number of attempts to recognize the face
        announce(f"Please wait for {name} to be called...")
        print(f"Please wait for {name} to be called...")
        start_time = time.time()
        while time.time() - start_time <= 60:  # Run for 60 seconds
            ret, frame = video_capture.read()
            if not ret:
                print("Error: Could not read frame")
                continue

            # Apply convolution methods for preprocessing (e.g., edge detection, blurring, etc.)
            # Example:
            # frame = cv2.Canny(frame, 100, 200)  # Apply Canny edge detection

            # Convert frame to RGB for face recognition
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Find face locations and encodings in the frame
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # If there are no face detections, increment attempts
            if len(face_locations) == 0:
                attempts += 1

            # Loop through detected faces
            for face_encoding, face_location in zip(face_encodings, face_locations):
                # Compare face encoding with known encodings
                matches = face_recognition.compare_faces([known_face_encodings[known_faces_names.index(name)]], face_encoding)
                if True in matches:
                    announce(f"Recognized: {name}")
                    print(f"Recognized: {name}")

                    # Write attendance to CSV file
                    with open(csv_filename, 'a', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow([name, 'Present'])

                    # Insert attendance into MySQL
                    sql = "INSERT INTO attendance (name, status, date) VALUES (%s, %s, %s)"
                    val = (name, 'Present', datetime.now().date())
                    mycursor.execute(sql, val)
                    mydb.commit()

                    recognized = True
                    if text == f"{name} recognized":
                        print(f"{name} recognized.")
                        break  # Exit the loop once a face is recognized

            # Draw a text on the frame if the person is not recognized
            if not recognized:
                # Draw a black rectangle
                cv2.rectangle(frame, (100, 50), (frame.shape[1] - 100, 100), (0, 0, 0), -1)
                # Put the text in the center of the rectangle
                text = f"{name} not recognized"
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                text_x = (frame.shape[1] - text_size[0]) // 2
                text_y = 85  # Adjusted position to be closer to the top
                cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            cv2.imshow("Attendance System", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if recognized:
                if text == f"{name} recognized":
                    # Perform actions when recognized
                    # For example:
                    print(f"{name} recognized.")
                    # You can add more actions here
                break  # Exit the loop if a face is recognized

        # Display alert message if the person is not recognized after the loop
        if not recognized and attempts >= 3:
            # Write attendance to CSV file
            with open(csv_filename, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([name, 'Absent'])

            # Insert absent students into MySQL
            sql = "INSERT INTO attendance (name, status, date) VALUES (%s, %s, %s)"
            val = (name, 'Absent', datetime.now().date())
            mycursor.execute(sql, val)
            mydb.commit()

            announce(f"Alert: {name} not detected after multiple attempts. Marked as absent.")
            print(f"Alert: {name} not detected after multiple attempts. Marked as absent.")

        elif not recognized:
            announce(f"{name} not recognized. Marked as absent.")
            print(f"{name} not recognized. Marked as absent.")

    # Release the video capture device
    video_capture.release()
    cv2.destroyAllWindows()

    announce(f"Attendance recorded in {csv_filename}")
    print(f"Attendance recorded in {csv_filename}")

    return 'Attendance recording initiated.'

if __name__ == '__main__':
    app.run(debug=True)
