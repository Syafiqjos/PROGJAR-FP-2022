import pygame
import random

from Library.Sprite import Sprite

class MatahariOrb(Sprite):
	def __init__(self, screen, position):
		super().__init__(screen, position, (1, 1), 'Assets/kenney_pixelshmup/Ships/ship_0000.png')

	def awake(self):
		self.stopFallPos = 120 + random.random() * 290
		self.destroyTimer = 500

	def setup(self, scene):
		self.scene = scene

	def update(self):
		if self.position[1] < self.stopFallPos:
			self.setPosition((self.position[0], self.position[1] + 1))
		if self.destroyTimer > 0:
			self.destroyTimer -= 1
		else:
			self.destroy()

	def destroy(self):
		if self.scene.state == 'PLANTS':
			if self in self.scene.plantsOrbs:
				self.scene.plantsOrbs.remove(self)
				del self
		elif self.scene.state == 'ZOMBIES':
			if self in self.scene.zombiesOrbs:
				self.scene.zombiesOrbs.remove(self)
				del self

class PeluruBuncis(Sprite):
	def __init__(self, screen, position):
		super().__init__(screen, position, (1, 1), 'Assets/gameicons/PNG/White/1x/minus.png')

	def awake(self):
		self.bulletSpeed = 2
		self.bulletDamage = 25

	def setup(self, scene):
		self.scene = scene

	def update(self):
		self.setPosition((self.position[0] + self.bulletSpeed, self.position[1]))
		if self.position[0] > 800:
			self.destroy()

	def destroy(self):
		if self in self.scene.plantsBullets:
			self.scene.plantsBullets.remove(self)
			del self

class Tumbuhan(Sprite):
	def __init__(self, screen, position, scale, imagePath):
		super().__init__(screen, position, scale, imagePath)
		self.healthTotal = 100

	def update(self):
		if self.collideWithZombie():
			pass

	def collideWithZombie(self):
		for zombie in self.scene.sprites['ALLZOMBIES']:
			if self.rect.colliderect(zombie.rect):
				self.healthTotal -= zombie.eatingRate
				zombie.stopForAWhile()

		if self.healthTotal <= 0:
			self.destroy()

	def destroy(self, forced = False):
		if forced or self.scene.state == 'PLANTS':
			if self.spriteName in self.scene.objects:
				self.scene.triggerPlantDie(self.scene.objects[self.spriteName])
				self.scene.sprites['ALLPLANTS'].remove(self.scene.objects[self.spriteName])
				del self.scene.objects[self.spriteName]

class TumbuhanKentang(Tumbuhan):
	def __init__(self, screen, position):
		super().__init__(screen, position, (1, 1), 'Assets/kenney_pixelshmup/Ships/ship_0001.png')
		self.type = 'plants_potato'

	def awake(self):
		super().awake()
		self.plantsMatahariTimerMax = 400
		self.plantsMatahariTimer = self.plantsMatahariTimerMax

	def setup(self, spriteName, scene):
		self.spriteName = spriteName
		self.scene = scene
		self.plantsSpawnMatahari = self.scene.plantsSpawnMatahari

	def spawnMatahari(self):
		matahari = self.plantsSpawnMatahari((self.position[0], self.position[1] - 10))
		matahari.stopFallPos = self.position[1] + 10

	def update(self):
		super().update()
		if self.plantsMatahariTimer > 0:
			self.plantsMatahariTimer -= 1
		else:
			self.plantsMatahariTimer = self.plantsMatahariTimerMax
			# self.spawnMatahari()

class TumbuhanBuncisNormal(Tumbuhan):
	def __init__(self, screen, position):
		super().__init__(screen, position, (1, 1), 'Assets/kenney_pixelshmup/Ships/ship_0002.png')
		self.type = 'plants_pea'

	def awake(self):
		super().awake()
		self.plantsShootTimerMax = 200
		self.plantsShootTimer = self.plantsShootTimerMax

	def setup(self, spriteName, scene):
		self.spriteName = spriteName
		self.scene = scene

	def shoot(self, forced = False):
		if forced or self.scene.state == 'PLANTS':
			bullet = PeluruBuncis(self.screen, (self.position[0], self.position[1] - 10))
			bullet.setup(self.scene)
			self.scene.plantsBullets.append(bullet)
			self.scene.triggerPlantShoot(self)

	def update(self):
		super().update()
		if self.plantsShootTimer > 0:
			self.plantsShootTimer -= 1
		else:
			self.plantsShootTimer = self.plantsShootTimerMax
			self.shoot()

class TumbuhanBuncisJago(Tumbuhan):
	def __init__(self, screen, position):
		super().__init__(screen, position, (1, 1), 'Assets/kenney_pixelshmup/Ships/ship_0003.png')
		self.type = 'plants_repeater'

	def awake(self):
		super().awake()
		self.plantsShootTimerMax = 200
		self.plantsShootTimerMaxShort = 25
		self.plantsShootCount = 0
		self.plantsShootTimer = self.plantsShootTimerMax

	def setup(self, spriteName, scene):
		self.spriteName = spriteName
		self.scene = scene

	def shoot(self, forced = False):
		if forced or self.scene.state == 'PLANTS':
			bullet = PeluruBuncis(self.screen, (self.position[0], self.position[1] - 10))
			bullet.setup(self.scene)
			self.scene.plantsBullets.append(bullet)
			self.plantsShootCount += 1
			self.scene.triggerPlantShoot(self)

	def update(self):
		super().update()
		if self.plantsShootTimer > 0:
			self.plantsShootTimer -= 1
		else:
			if self.plantsShootCount % 2 == 0:
				self.plantsShootTimer = self.plantsShootTimerMaxShort
			else:
				self.plantsShootTimer = self.plantsShootTimerMax
			self.shoot()

class ZombieWalker(Sprite):
	def __init__(self, screen, position, scale, imagePath):
		super().__init__(screen, position, scale, imagePath)

	def awake(self):
		self.healthTotal = 100
		self.walkingSpeed = 0.25
		self.eatingRate = 1

		self.stopInterval = 0

		self.walkTransmitIntervalMax = 120
		self.walkTransmitInterval = 120

	def setup(self, spriteName, scene):
		self.spriteName = spriteName
		self.scene = scene

	def update(self):
		# check got shoot by peluru tumbuhan
		if self.collideWithBullet():
			pass
		# check if not out of bound on left yet then walk to the left
		elif self.position[0] > 10:
			self.checkWalk()
		else:
			# eat brain and win the current lane
			self.scene.triggerZombiesWin()

	def stopForAWhile(self):
		self.stopInterval = 20

	def checkWalk(self):
		if self.stopInterval <= 0:
			self.walk()
		else:
			self.stopInterval -= 1

	def walk(self):
		self.setPosition((self.position[0] - self.walkingSpeed, self.position[1]))

		if self.walkTransmitInterval > 0:
			self.walkTransmitInterval -= 1
		else:
			self.scene.triggerZombieMove(self)
			self.walkTransmitInterval = self.walkTransmitIntervalMax

	def collideWithBullet(self):
		for bullet in self.scene.plantsBullets:
			if self.rect.colliderect(bullet.rect):
				self.healthTotal -= bullet.bulletDamage
				bullet.destroy()

		if self.healthTotal <= 0:
			self.destroy()

	def destroy(self, forced = False):
		if forced or self.scene.state == 'ZOMBIES':
			if self.spriteName in self.scene.objects:
				self.scene.triggerZombieDie(self.scene.objects[self.spriteName])
				self.scene.sprites['ALLZOMBIES'].remove(self.scene.objects[self.spriteName])
				del self.scene.objects[self.spriteName]

class ZombieWalkerNormal(ZombieWalker):
	def __init__(self, screen, position):
		super().__init__(screen, position, (0.08, 0.08), 'Assets/robotball/skeleton-animation_01.png')
		self.type = 'zombies_normal'

	def awake(self):
		super().awake()
		self.healthTotal = 100
		self.walkingSpeed = 0.25

class ZombieWalkerJago(ZombieWalker):
	def __init__(self, screen, position):
		super().__init__(screen, position, (0.08, 0.08), 'Assets/robotball/skeleton-animation_03.png')
		self.type = 'zombies_cone'

	def awake(self):
		super().awake()
		self.healthTotal = 250
		self.walkingSpeed = 0.25

class ZombieWalkerHandal(ZombieWalker):
	def __init__(self, screen, position):
		super().__init__(screen, position, (0.08, 0.08), 'Assets/robotball/skeleton-animation_05.png')
		self.type = 'zombies_bucket'

	def awake(self):
		super().awake()
		self.healthTotal = 500
		self.walkingSpeed = 0.25