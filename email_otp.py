import random, os, smtplib

def generateOTP(otp_size = 6):
    """Random number generator to create One-Time-Password"""
    final_otp = ''
    for i in range(otp_size):
        final_otp = final_otp + str(random.randint(0,9))
    return final_otp

def sendEmailVerificationRequest(sender="DEFAULT_SENDER", receiver="DEFAULT_RECEIVER"):
    """Sends OTP email to receiver"""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    google_app_password = os.getenv("PASSWORD")
    server.login(sender, google_app_password)
    cur_otp = generateOTP()
    msg = "Hello, Your OTP is " +  cur_otp
    server.sendmail(sender,receiver,msg)
    server.quit()
    return cur_otp