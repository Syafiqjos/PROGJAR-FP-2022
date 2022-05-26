import dotenv
import socket
import os
import utils

BUFF_SIZE = 2048
PORT = 8080
BACKLOG = socket.SOMAXCONN
SELECT_TIMEOUT = 0.5
AVAILABLE_ACTIONS = {
    "register": None,
    "login": None,
    "find_match": None,
    "cancel_find_match": None,
}
email = ""
password = ""


def init():
    global email, password

    dotenv.load_dotenv()
    email = os.getenv("EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    utils.email.initialize_email_service()


def get_email():
    return email


def get_password():
    return password
