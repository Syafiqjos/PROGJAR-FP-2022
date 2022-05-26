import traceback
import json
import select
import config
import controllers
import utils

from utils.error import AppError
from utils.socket import send

connections = []


if __name__ == "__main__":
    config.init()
    zombie_queue = []
    plant_queue = []

    server = utils.socket.start_server(config.PORT, config.BACKLOG)
    connections.append(server)
    print(f"Server started on port {config.PORT}!\n")

    i = 1
    while True:
        print(f"Waiting for ready sockets {i}...")
        i += 1
        rlist, wlist, xlist = select.select(connections, [], [], config.SELECT_TIMEOUT)

        for ready_socket in rlist:
            if ready_socket == server:
                print("New client connected!!\n")
                client, addr = ready_socket.accept()
                connections.append(client)
                continue

            # Accept trigger from client
            raw = ready_socket.recv(config.BUFF_SIZE)
            if not raw:
                # Client has disconnected
                print("Client disconnected :(\n")
                connections.remove(ready_socket)
                continue

            # Check request
            data = json.loads(raw)
            request = data.get("request", "")

            if request not in config.AVAILABLE_ACTIONS:
                print("Invalid request!\n")
                send(ready_socket, {"error": "Invalid request!"})
                continue

            # Call handler
            try:
                if request == "register":
                    controllers.register(ready_socket, data)
                if request == "login":
                    controllers.login(ready_socket, data)
                if request == "find":
                    controllers.find_match(
                        ready_socket,
                        data.get("role"),
                        connections,
                        plant_queue,
                        zombie_queue,
                    )
                if request == "cancel":
                    controllers.cancel_find_match()
            except (AppError, Exception) as e:
                traceback.print_exc()
                e = e.__dict__
                data = {
                    "error": e.get("message", "Error"),
                    "code": e.get("status_code", 500),
                }
                send(ready_socket, data)
