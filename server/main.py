import traceback
import json
import select
import config
import controllers
import utils

from utils.error import AppError
from utils.socket import send

connections = []


def main():
    config.init()
    zombie_queue = []
    plant_queue = []

    config.AVAILABLE_ACTIONS["register"] = controllers.register
    config.AVAILABLE_ACTIONS["login"] = controllers.login
    config.AVAILABLE_ACTIONS["find_match"] = controllers.find_match
    config.AVAILABLE_ACTIONS["cancel_find_match"] = controllers.cancel_find_match

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
                print("Client disconnected :(\n")
                connections.remove(ready_socket)
                continue

            # Check request
            data = json.loads(raw)
            request = data.get("request", "")

            if request not in config.AVAILABLE_ACTIONS:
                send(ready_socket, {"error": "Unknown request!"})
                continue

            # Call handler
            try:
                config.AVAILABLE_ACTIONS[request](
                    client=ready_socket,
                    data=data,
                    connections=connections,
                    plant_queue=plant_queue,
                    zombie_queue=zombie_queue,
                )
            except AppError as e:
                traceback.print_exc()
                send(ready_socket, e.payload)
            except Exception as e:
                traceback.print_exc()
                send(ready_socket, {"error": "Internal server error"})


if __name__ == "__main__":
    main()
