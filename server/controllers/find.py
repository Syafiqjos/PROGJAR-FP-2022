import os
import threading
import socket
import jwt
import games

from utils.socket import send
from utils.error import AppError


def find_match(
    client: socket.socket = None,
    data: dict = {},
    connections: list = None,
    plant_queue: list = None,
    zombie_queue: list = None,
    *args,
    **kwargs
):
    token = data.get("token", "")
    if not token:
        raise AppError("Token is required!")

    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        raise AppError("Invalid token!")

    role = data.get("role", "")
    if role not in ["zombie", "plant"]:
        raise AppError("Role should be plant or zombie")

    if client in plant_queue or client in zombie_queue:
        raise AppError("You are already in queue")

    queue = {"plant": plant_queue, "zombie": zombie_queue}
    queue[role].append({"email": payload.get("sub"), "socket": client})

    if len(plant_queue) < 1 or len(zombie_queue) < 1:
        send(client, {"success": True, "match_status": "waiting"})
        return

    plant: dict = plant_queue.pop(0)
    zombie: dict = zombie_queue.pop(0)

    send(
        plant["socket"],
        {"success": True, "match_status": "found", "enemy": zombie["email"]},
    )
    send(
        zombie["socket"],
        {"success": True, "match_status": "found", "enemy": plant["email"]},
    )

    # Remove from connections so that any data sent by the client is ignored in the main
    # Later, when the game is over, those clients will be added back to the connections
    connections.remove(plant["socket"])
    connections.remove(zombie["socket"])

    # Start game
    thread = threading.Thread(
        target=games.pvz.start_game, args=(plant, zombie, connections)
    )
    thread.start()
