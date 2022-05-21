from Manager.GameManager import GameManager
from Manager.DataManager import DataManager
from Manager.EventManager import EventManager
from Scene.MainMenu import MainMenu

dataManager = DataManager()
eventManager = EventManager()
gameManager = GameManager(dataManager, eventManager, [720, 480])

gameManager.loadScene(MainMenu)
gameManager.run()