import select
import socket
import threading

def cancel_find():
    # TODO: complete this function
    pass

def find(player: socket.socket, role: str, connections: list, plant_queue: list, zombie_queue: list):
    if role != 'plant' or role != 'zombie':
        # TODO: handle invalid role
        return

    queue = { 'plant': plant_queue, 'zombie': zombie_queue }
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

# ? Apakah list_connection reference tetap bekerja jika dipassing ke thread
# Kalo ngga bisa, terpaksa start game harus di start dari main supaya bisa access global variable connections
def start_game(plant, zombie, list_connection):
    # TODO: complete this function
    while True:
        print('(from thread) Waiting for ready connection...')
        rlist, wlist, xlist = select.select([plant, zombie], [], [])
        for ready in rlist:
            raw = ready.recv(BUFF_SIZE)

            # If client has disconnected
            if not raw:
                # handle disconnection
                print('(from thread) Client disconnected! Exiting thread..\n')
                return
            
            print('(from thread) Client sent something\n')

