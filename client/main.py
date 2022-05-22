from Manager.GameManager import GameManager
from Manager.DataManager import DataManager
from Manager.EventManager import EventManager
from Scene.MainMenu import MainMenu
from Scene.LobbyMenu import LobbyMenu
from Scene.GameplayScene import GameplayScene

dataManager = DataManager()
eventManager = EventManager()
gameManager = GameManager(dataManager, eventManager, [720, 480])
gameManager.registerScene('MainMenu', MainMenu);
gameManager.registerScene('LobbyMenu', LobbyMenu);
gameManager.registerScene('GameplayScene', GameplayScene);

gameManager.loadScene('GameplayScene')
gameManager.run()