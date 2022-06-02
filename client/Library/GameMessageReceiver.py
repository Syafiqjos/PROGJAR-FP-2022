import json
import threading
import time

from .MessageReceiver import MessageReceiver

class GameMessageReceiver(MessageReceiver):
	def __init__(self, sock):
		super().__init__(sock);
		self.eventListener = None

	def subscribeEventListener(self, func):
		self.eventListener = func

	def run(self):
		print('run thread message receiver')
		try:
			while self.running:
				# data = { 'message': 'lol' }
				data = self.sock.recv(1024)
				data = data.decode()

				# print(data)
				# time.sleep(1)
				# print('some sleeping thread...')

				if self.eventListener is not None:
					jsonData = json.loads(data)
					self.eventListener(jsonData)

				
		except Exception as e:
			print(e)