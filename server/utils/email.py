import os
import config
import smtplib

server = None


def initialize_email_service():
    global server

    username = config.get_email()
    password = config.get_password()

    print("Login to email service...")
    server = smtplib.SMTP_SSL(
        os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_HOST_PORT"))
    )
    server.ehlo()
    server.login(username, password)


def send_email(to, message):
    global server

    TO_EMAIL_ADDRESS = to
    FROM_EMAIL_ADDRESS = config.get_email()

    server.sendmail(FROM_EMAIL_ADDRESS, TO_EMAIL_ADDRESS, message)
