import random, os, smtplib

sender = os.getenv("EMAIL_ADDRESS")
password = os.getenv("PASSWORD")

def generateOTP(otp_size = 6):
    """Random number generator to create One-Time-Password"""
    final_otp = ''
    for i in range(otp_size):
        final_otp = final_otp + str(random.randint(0,9))
    return final_otp

def sendEmailVerificationRequest(sender=sender, receiver="DEFAULT_RECEIVER"):
    """Sends OTP email to receiver"""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    cur_otp = generateOTP()
    
    # Creates email subject and body with OTP
    msg = f"Subject: Your OTP Password\n\nThank you for signing up!\nYour OTP is: {cur_otp}"
    server.sendmail(sender, receiver, msg)
    server.quit()
    return cur_otp
