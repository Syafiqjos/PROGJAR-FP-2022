import threading
import socket


def find_match(
    player: socket.socket,
    role: str,
    connections: list,
    plant_queue: list,
    zombie_queue: list,
):
    if role != "plant" or role != "zombie":
        # TODO: handle invalid role
        return

    queue = {"plant": plant_queue, "zombie": zombie_queue}
    queue[role].append(player)

    if len(plant_queue) > 0 and len(zombie_queue) > 0:
        plant: socket.socket = plant_queue.pop(0)
        zombie: socket.socket = zombie_queue.pop(0)

        # Remove from connections so that any data sent by the client is ignored in the main
        # Later, when the game is over, those clients will be added back to the connections
        connections.remove(plant)
        connections.remove(zombie)

        # Start game
        thread = threading.Thread(target=start_game, args=(plant, zombie, connections))
        thread.start()
