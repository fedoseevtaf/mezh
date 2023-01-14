import pygame

from uiboard import UIBoard
from r_ui.base import BorderedContainer
from r_ui.text import TextString
from r_ui.advanced import (
	TextButton, UpArrowButton, DownArrowButton, ImageButton
)


FPS = 60
CAPTION = 'Mezh Tetravex!'
RESOLUTION = W, H = 1920, 1080
DISPLAY_MODE = pygame.SCALED | pygame.RESIZABLE


def main(app):
	pygame.display.set_mode(RESOLUTION, DISPLAY_MODE)
	pygame.display.set_caption(CAPTION)
	clock = pygame.time.Clock()
	
	app.init()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return app.quit()
			app.event(event)
		pygame.display.flip()
		app.step(clock.tick(FPS))
		
		
class App():
	
	def init(self):
		pass
		
	def event(self, event: pygame.event.EventType):
		pass
		
	def step(self, delta: float):
		pass
		
	def quit(self):
		pass


if __name__ == '__main__':
	pygame.init()
	app = App()
	main(app)
	pygame.quit()

