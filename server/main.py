import json
import socket
import select
import threading
from utils.server import start_server
from utils.auth import login, register
from utils.game import find, cancel_find

PORT = 8080
BACKLOG = socket.SOMAXCONN
BUFF_SIZE = 2048
SELECT_TIMEOUT = 1
AVAILABLE_ACTIONS = [
    'register',
    'login',
    'find',
    'cancel',
]
connections = []

if __name__ == '__main__':
    zombie_queue = []
    plant_queue = []

    server = start_server(PORT, BACKLOG)
    connections.append(server)
    print('Server started on port {}!\n'.format(PORT))

    while True:
        print('(main) Waiting for ready sockets...')
        rlist, wlist, xlist = select.select(connections, [], [], SELECT_TIMEOUT)
        for ready_socket in rlist:
            if ready_socket == server:
                print('(main) New client connected!!\n')
                client, addr = ready_socket.accept()
                connections.append(client)
                continue

            # Accept trigger from client
            raw = ready_socket.recv(BUFF_SIZE)
            if not raw:
                # Client has disconnected
                print('(main) Client disconnected :(\n')
                connections.remove(ready_socket)
                continue

            # Check request
            data = json.loads(raw)
            request = data.get('request', '')

            if request not in AVAILABLE_ACTIONS:
                print('(main) Invalid request!\n')
                ready_socket.send(json.dumps({'error': 'Invalid request!'}).encode())
                continue

            # Call handler
            if request == 'register':
                register(ready_socket, data.get('email'), data.get('password'))
            if request == 'login':
                login(ready_socket, data.get('email'), data.get('password'))
            if request == 'find':
                find(ready_socket, data.get('role'), connections, plant_queue, zombie_queue)
            if request == 'cancel':
                cancel_find()