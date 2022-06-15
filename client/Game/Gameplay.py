import sys
sys.path.append('..')

from manager.GameManager import GameManager
from manager.DataManager import DataManager
from manager.EventManager import EventManager
from scene.MainMenu import MainMenu
from scene.LobbyMenu import LobbyMenu
from scene.ScoreMenu import ScoreMenu
from scene.GameplayScene import GameplayScene

def game(dataManager, socketManager, accountSocket, gameSocket):
	eventManager = EventManager()
	gameManager = GameManager(dataManager, eventManager, [720, 480], socketManager, accountSocket, gameSocket)
	gameManager.registerScene('MainMenu', MainMenu);
	gameManager.registerScene('LobbyMenu', LobbyMenu);
	gameManager.registerScene('GameplayScene', GameplayScene);
	gameManager.registerScene('ScoreMenu', ScoreMenu);

	gameManager.loadScene('MainMenu')
	gameManager.run()