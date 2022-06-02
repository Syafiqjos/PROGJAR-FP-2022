from .SocketSender import SocketSender;

class GameSocket(SocketSender):
	def sendZombieSpawnEvent(self, tile, zombie):
		return self.send({
			"event": "on_zombie_spawn",
			"zombie": {
				"id": zombie.spriteName,
				"type": zombie.type,
				"pos": {
					"x": zombie.position[0],
					"y": zombie.position[1]
				},
				"tile": {
					"x": 4,
					"y": 1
				}
			}
		}, False)

	def sendPlantSpawnEvent(self, tile, plant):
		return self.send({
			"event": "on_plant_spawn",
			"plant": {
				"id": plant.spriteName,
				"type": plant.type,
				"pos": {
					"x": plant.position[0],
					"y": plant.position[1]
				},
				"tile": {
					"x": 4,
					"y": 1
				}
			}
		}, False)

	def sendZombieMoveEvent(self, tile, zombie):
		return self.send({
			"event": "on_zombie_move",
			"zombie": {
				"id": zombie.spriteName,
				"pos": {
					"x": zombie.position[0],
					"y": zombie.position[1]
				},
				"tile": {
					"x": 4,
					"y": 1
				}
			}
		}, False)

	def sendZombieAttackEvent(self, zombie, plant):
		return self.send({
			"event": "on_zombie_move",
			"zombie": {
				"id": zombie.spriteName
			},
			"plant": {
				"id": plant.spriteName
			}
		}, False)

	def sendZombieDieEvent(self, zombie):
		return self.send({
			"event": "on_zombie_die",
			"zombie": {
				"id": zombie.spriteName
			}
		}, False)

	def sendPlantDieEvent(self, plant):
		return self.send({
			"event": "on_plant_die",
			"plant": {
				"id": plant.spriteName
			}
		}, False)

	def sendPlantShootEvent(self, plant):
		return self.send({
			"event": "on_plant_shoot",
			"plant": {
				"id": plant.spriteName
			}
		}, False)

	def sendPlantAttackEvent(self, plant, zombie):
		return self.send({
			"event": "on_plant_attack",
			"plant": {
				"id": plant.spriteName
			},
			"zombie": {
				"id": zombie.spriteName
			}
		}, False)

	def sendWinnerEvent(self, winner):
		return self.send({
			"event": "on_winner",
			"winner": winner
		}, False)