import select
import config
import json

from utils.socket import send


def start_game(
    plant: dict = {"email": "", "socket": None},
    zombie: dict = {"email": "", "socket": None},
    connections: list = [],
):
    plant_email, plant_sock = plant["email"], plant["socket"]
    zombie_email, zombie_sock = zombie["email"], zombie["socket"]

    while True:
        rlist, _wlist, _xlist = select.select([plant_sock, zombie_sock], [], [])
        for ready in rlist:
            raw = ready.recv(config.BUFF_SIZE)
            if not raw:
                print("(from thread) Client disconnected! Exiting thread..\n")
                pair = plant_sock if ready == zombie_sock else zombie_sock
                send(pair, {"event": "on_disconnect"})
                connections.append(pair)
                return

            print("(from thread) Client sent something\n")
            pair = plant_sock if ready == zombie_sock else zombie_sock
            data = json.loads(raw)
            send(pair, data)
