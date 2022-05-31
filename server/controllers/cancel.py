import socket
from utils.socket import send


def cancel_find_match(
    client: socket.socket, plant_queue: list, zombie_queue: list, *args, **kwargs
):
    if client in plant_queue:
        plant_queue.remove(client)
    if client in zombie_queue:
        zombie_queue.remove(client)

    send(client, {"success": True})
