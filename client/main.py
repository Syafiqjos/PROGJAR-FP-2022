from scene.MainMenu import MainMenu

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([1280, 720])
scene = MainMenu(screen)

# Run until the user asks to quit
running = True
while running:
	# Did the user click the window close button?
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	if scene is not None:
		scene.render()

	pygame.display.flip()

pygame.quit()