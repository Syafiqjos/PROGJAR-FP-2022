import socket

def start_server(port: int = 8080, backlog: int = 10) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', port))
    sock.listen(backlog)

    print('Server started on port {}'.format(port))
    return sock
