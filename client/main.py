from Manager.GameManager import GameManager
from Manager.DataManager import DataManager
from Scene.MainMenu import MainMenu

dataManager = DataManager()
gameManager = GameManager(dataManager, [720, 480])

gameManager.loadScene(MainMenu)
gameManager.run()