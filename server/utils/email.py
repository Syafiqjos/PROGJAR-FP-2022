import os
import config
import smtplib

server = None


def initialize_email_service():
    global server

    username = config.get_email()
    password = config.get_password()
    email_host = os.getenv("EMAIL_HOST")
    email_port = int(os.getenv("EMAIL_HOST_PORT"))

    print("Login to email service...")
    server = smtplib.SMTP_SSL(email_host, email_port)
    server.ehlo()
    server.login(username, password)


def send_email(to, subject="", content="", footer=""):
    global server

    TO_EMAIL_ADDRESS = to
    FROM_EMAIL_ADDRESS = config.get_email()
    message = "Subject: {}\n\n{}\n\n{}".format(subject, content, footer)
    server.sendmail(FROM_EMAIL_ADDRESS, TO_EMAIL_ADDRESS, message)
