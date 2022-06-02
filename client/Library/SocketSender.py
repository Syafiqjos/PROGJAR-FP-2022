class SocketSender():
	def __init__(self, socketManager):
		self.socketManager = socketManager

	def send(self, data, syncReceive = True):
		self.socketManager.send(data)
		if syncReceive != True:
			return None
		data = self.socketManager.receive()
		return data