"""
Creating a separate module for sending the e-mail to the users. You take care not to name the module like "email"
or other module names like scripts names.
mime.text has to be imported in order to be able to use it in HTML
To be able to login via smtlip: In gmail Options - Security/Less secure app access panel - click Turn on access

SENDING EMAIL function is always similar (see the script)
"""
from email.mime.text import MIMEText
import smtplib


def send_email(email, height, average_height, count):
    from_email="xxxxxxxxxx@gmail.com"   # send from this email
    from_password="xxxxxxxxxx"          # email with this password
    to_email=email                      # entered email

    subject="Height data"               # the subject of the email
    message="Hi there, your height is <strong>%s</strong>. <br> " \
            "Average height of all is <strong>%s</strong> " \
            "and this is calculated out of <strong>%s</strong> people. <br> Thanks!" % (height, average_height, count)
                                                                    # the text of the email (it has HTML bold tags)

    msg=MIMEText(message, 'html')   # message will be red as HTML, so we can use HTML tags inside the message
    msg['Subject']=subject          # 1. MIMEText key that we need to have
    msg['To']=to_email              # 2. MIMEText key that we need to have
    msg['From']=from_email          # 3. MIMEText key that we need to have

    gmail=smtplib.SMTP('smtp.gmail.com', 587)   # google: smtp gmail settings
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)      # login with our credentials
    gmail.send_message(msg)
