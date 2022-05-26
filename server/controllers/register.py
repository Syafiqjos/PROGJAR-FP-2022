import os
import socket
import json
import utils
from utils.error import AppError
from utils.socket import send


def register(client: socket.socket, data: dict):
    users_repo = os.getenv("REPO_LOCATION")
    password_length = int(os.getenv("USER_PASSWORD_LENGTH"))
    email = data.get("email", "")

    # check if email is empty
    if email == "":
        raise AppError(status_code=400, message="Email is empty!")

    with open(users_repo, "r") as f:
        repo = json.loads(f.read())
        users = repo.get("users", [])

    # check existing email
    existing_user = list(filter(lambda user: user.get("email", "") == email, users))
    if len(existing_user) > 0:
        raise AppError(status_code=422, message="Email is already registered!")

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
    send(client, {"message": "Check email for your password!"})
