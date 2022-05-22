from Manager.GameManager import GameManager
from Manager.DataManager import DataManager
from Manager.EventManager import EventManager
from Scene.MainMenu import MainMenu
from Scene.LobbyMenu import LobbyMenu

dataManager = DataManager()
eventManager = EventManager()
gameManager = GameManager(dataManager, eventManager, [720, 480])
gameManager.registerScene('MainMenu', MainMenu);
gameManager.registerScene('LobbyMenu', LobbyMenu);

gameManager.loadScene('MainMenu')
gameManager.run()