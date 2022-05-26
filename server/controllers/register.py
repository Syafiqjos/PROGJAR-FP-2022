import os
import socket
import json
import utils
from utils.error import AppError
from utils.socket import send


def register(client: socket.socket = None, data: dict = {}, *args, **kwargs):
    users_repo = os.getenv("REPO_LOCATION")
    password_length = int(os.getenv("USER_PASSWORD_LENGTH"))
    email = data.get("email", "")

    # validate email
    if not utils.validation.is_email_valid(email):
        raise AppError("Email is invalid!")

    with open(users_repo, "r") as f:
        repo = json.loads(f.read())
        users = repo.get("users", [])

    # check existing email
    existing_user = list(filter(lambda user: user.get("email", "") == email, users))
    if len(existing_user) > 0:
        raise AppError("Email is already registered!")

    password = utils.random.random_string(password_length)
    repo["users"].append(
        {
            "email": email,
            "password": password,
        }
    )

    with open(users_repo, "w") as f:
        f.write(json.dumps(repo))

    utils.email.send_email(email, "This is = {}".format(password))
    send(client, {"success": True, "message": "Check email for your password"})
