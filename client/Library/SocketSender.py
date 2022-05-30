class SocketSender():
	def __init__(self, socketManager):
		self.socketManager = socketManager

	def send(self, data):
		self.socketManager.send(data)
		data = self.socketManager.receive()
		return data