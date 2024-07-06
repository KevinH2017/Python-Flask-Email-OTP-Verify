from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from email_otp import *
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(12)
# Changes directory of where data.db is stored and used from
# app.root_path is absolute path to current python app directory
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.root_path}/instance/email.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"                # Change to fit your email server
app.config["MAIL_PORT"] = 587   # 465 for SMTP, 587 for TLS
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_ADDRESS")            # Sender email address set in Environment Variables
app.config["MAIL_PASSWORD"] = os.getenv("PASSWORD")                 # Sender email password set in Environment Variables
app.config["MAIL_USE_TLS"] = True

db = SQLAlchemy(app)

mail = Mail(app)

class Form(db.Model):
    """Creates columns and their datatypes inside email.db"""
    __tablename__ = "emails"
    id_num = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))

    def __init__(self, email):
        self.email = email


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route('/verify', methods=["POST"])  
def verify():  
    """Sends email with One-Time-Password code"""
    global rec_email 
    rec_email = request.form["email"]
       
    current_otp = sendEmailVerificationRequest(receiver=rec_email) # this function sends otp to the receiver and also returns the same otp for our session storage
    session['current_otp'] = current_otp
    return render_template('verify.html', email=rec_email)  


@app.route('/validate', methods=["POST"])
def validate():
    """Checks if OTP matches the current session"""
    # OTP that was sent to the receiver
    current_user_otp = session['current_otp']
    
    # OTP Entered by the User
    user_otp = request.form['otp'] 
     
    if int(current_user_otp) == int(user_otp):  
        email = rec_email                       # Gets email from global variable rec_email

        form = Form( 
            email=email, 
        )

        db.session.add(form)
        db.session.commit()

        message_body = "Thank you for subscribing to our mailing list!"
        message = Message("Welcome to Our Mailing list!",
                            sender=app.config["MAIL_USERNAME"], 
                            recipients=[email],
                            body=message_body)
        
        mail.send(message)
        return "<h3> Your email has been successfully verified! </h3>"  
    else:
        return "<h3> Oops! Email Verification Failure, OTP does not match. </h3>"   
    
 
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)