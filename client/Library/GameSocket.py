from .SocketSender import SocketSender;

class GameSocket(SocketSender):
	def sendZombieSpawnEvent(self, tile, zombie):
		tileCoords = tile.replace('all_bgTile', '')
		tileX = tileCoords.split('x')[0]
		tileY = tileCoords.split('x')[1]
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
					"x": tileX,
					"y": tileY
				}
			}
		}, False)

	def sendPlantSpawnEvent(self, tile, plant):
		tileCoords = tile.replace('all_bgTile', '')
		tileX = tileCoords.split('x')[0]
		tileY = tileCoords.split('x')[1]
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
					"x": tileX,
					"y": tileY
				}
			}
		}, False)

	def sendZombieMoveEvent(self, zombie):
		return self.send({
			"event": "on_zombie_move",
			"zombie": {
				"id": zombie.spriteName,
				"pos": {
					"x": zombie.position[0],
					"y": zombie.position[1]
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
			"event": "on_winner_new",
			"winner": winner
		}, False)

	def sendTimeSyncEvent(self, time):
		return self.send({
			"event": "on_time_sync",
			"time": time
		}, False)

	def sendDisconnectEvent(self):
		return self.send({
			"event": "on_disconnect"
		}, False)