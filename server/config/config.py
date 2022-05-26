import dotenv
import socket
import os
import utils

BUFF_SIZE = 2048
PORT = 8080
BACKLOG = socket.SOMAXCONN
SELECT_TIMEOUT = 0.5
AVAILABLE_ACTIONS = [
    "register",
    "login",
    "find_match",
    "cancel_find_match",
]
email = ""
password = ""


def init():
    global email, password

    dotenv.load_dotenv()
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    utils.email.initialize_email_service()


def get_email():
    return email


def get_password():
    return password
