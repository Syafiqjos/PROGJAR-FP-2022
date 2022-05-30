import socket
import json

class SocketManager():
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.server_address = (host, port)
		self.connected = False

	def connect(self):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect(self.server_address)
		self.connected = True

	def close(self):
		self.connection.close()

	def send(self, data):
		jsonData = json.dumps(data);
		encodedData = jsonData.encode()

		self.connection.send(encodedData)

	def receive(self):
		jsonData = self.connection.recv(1024)

		decodedData = jsonData.decode()
		data = json.loads(decodedData)

		return data