import socket
import select
from utils import utils


def start_game(plant: socket.socket, zombie: socket.socket, list_connection: list):
    # TODO: complete this function
    while True:
        print("(from thread) Waiting for ready connection...")
        rlist, wlist, xlist = select.select([plant, zombie], [], [])
        for ready in rlist:
            raw = ready.recv(BUFF_SIZE)

            # If client has disconnected
            if not raw:
                # handle disconnection
                print("(from thread) Client disconnected! Exiting thread..\n")
                return

            print("(from thread) Client sent something\n")
