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
		})

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
		})

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
		})

	def sendZombieAttackEvent(self, zombie, plant):
		return self.send({
			"event": "on_zombie_move",
			"zombie": {
				"id": zombie.spriteName
			},
			"plant": {
				"id": plant.spriteName
			}
		})

	def sendZombieDieEvent(self, zombie):
		return self.send({
			"event": "on_zombie_die",
			"zombie": {
				"id": zombie.spriteName
			}
		})

	def sendPlantDieEvent(self, plant):
		return self.send({
			"event": "on_plant_die",
			"plant": {
				"id": plant.spriteName
			}
		})

	def sendPlantShootEvent(self, plant):
		return self.send({
			"event": "on_plant_shoot",
			"plant": {
				"id": plant.spriteName
			}
		})

	def sendPlantAttackEvent(self, plant, zombie):
		return self.send({
			"event": "on_plant_attack",
			"plant": {
				"id": plant.spriteName
			},
			"zombie": {
				"id": zombie.spriteName
			}
		})

	def sendWinnerEvent(self, winner):
		return self.send({
			"event": "on_winner",
			"winner": winner
		})