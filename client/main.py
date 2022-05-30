import sys
from GUI.App import app
from Game.Gameplay import game
from manager.DataManager import DataManager
from Library.AccountSocket import AccountSocket
from Library.GameSocket import GameSocket
from manager.SocketManager import SocketManager

socketManager = None
accountSocket = None
gameSocket = None

dataManager = None

def initialize_connection():
	global socketManager
	global accountSocket
	global gameSocket
	global dataManager

	dataManager = DataManager()

	socketManager = SocketManager('127.0.0.1', 8080)
	socketManager.connect()

	accountSocket = AccountSocket(socketManager)
	gameSocket = GameSocket(socketManager)

def run_game():
	game(dataManager, socketManager, accountSocket, gameSocket)

def run_app():
	app(dataManager, socketManager, accountSocket, gameSocket)

def check_run_game():
	if dataManager != None:
		is_logined = dataManager.get('user_token') != ''
		if is_logined:
			run_game()

if __name__ == '__main__':
	initialize_connection()
	run_app()
	check_run_game()
	socketManager.close()