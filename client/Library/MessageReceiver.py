import json
import threading
import time

class MessageReceiver(threading.Thread):
	def __init__(self, sock):
		self.sock = sock
		self.running = True
		threading.Thread.__init__(self)

	def close(self):
		self.running = False

	def run(self):
		print('run thread message receiver')
		try:
			while self.running:
				data = self.sock.recv(1024)
				data = data.decode()

				print(data)
				# time.sleep(1)
				print('some sleeping thread...')

				
		except Exception as e:
			print(e)