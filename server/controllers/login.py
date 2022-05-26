import os
import socket
import json
import jwt

from utils.socket import send
from utils.error import AppError


def login(client: socket.socket = None, data: dict = {}, *args, **kwargs):
    email = data.get("email", "")
    password = data.get("password", "")

    if not email or not password:
        raise AppError("Email and password are required!")

    users_repo = os.getenv("REPO_LOCATION")
    with open(users_repo, "r") as f:
        repo = json.loads(f.read())
        users = repo.get("users", [])

    user = list(filter(lambda user: user.get("email", "") == email, users))
    if len(user) == 0:
        raise AppError("Email is not registered!")

    user = user[0]
    if user.get("password", "") != password:
        raise AppError("Wrong password!")

    token = jwt.encode({"sub": email}, os.getenv("JWT_SECRET"), algorithm="HS256")
    send(client, {"success": True, "token": token})
