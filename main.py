from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from email_otp import sendEmailVerificationRequest
import os

app = Flask(__name__)

# Sets configuration for app
app.config.update(dict(
    SECRET_KEY = os.urandom(12),
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{app.root_path}/instance/email.db",
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 587,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = os.getenv("EMAIL_ADDRESS"),
    MAIL_PASSWORD = os.getenv("PASSWORD"),
    MAIL_USE_TLS = True
))

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
    """Sends email with One-Time password (OTP)"""
    global rec_email 
    rec_email = request.form["email"]
       
    # Sends OTP to receiver then sets OTP to session as 'current_otp'
    current_otp = sendEmailVerificationRequest(sender=app.config["MAIL_USERNAME"], receiver=rec_email) 
    session['current_otp'] = current_otp
    return render_template('verify.html')  


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
        return render_template("success.html") 
    else:
        return render_template("error.html") 
    
 
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)    # Runs on local 127.0.0.1 network
        # app.run(host="0.0.0.0")         # Opens webpage to entire network (Uses host IPv4 address)