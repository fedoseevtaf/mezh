from typing import Set

import pygame

from uiboard import UIBoard
from r_ui.base import UIElement, BorderedContainer
from r_ui.text import TextString
from r_ui.advanced import (
	TextField, TextButton, UpArrowButton, DownArrowButton, ImageButton
)


FPS = 60
ICON = 'img/icon.png'
CAPTION = 'Mezh Tetravex!'
RESOLUTION = W, H = 640, 360
DISPLAY_MODE = pygame.SCALED | pygame.RESIZABLE


def main(app):
	pygame.display.set_mode(RESOLUTION, DISPLAY_MODE)
	icon = pygame.image.load(ICON).convert_alpha()
	pygame.display.set_icon(icon)
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

	def __init__(self):
		# Behavior
		self.size = 3
		self._size_range = range(2, 6)
		self._WIN_TEXT = 'WIN!'
		# UI details
		self._screen: pygame.Surface = None
		self._back_color = 'Gray'
		self._front_color = 'Ivory'
		self._text_color = 'Black'
		# UIElements
		self._visible_elements: Set[UIElement] = set()

		self._central_text: TextString = None

		self._board: UIBoard = None
		self._board_pad: BorderedContainer = None

		self._restart_text: TextButton = None
		self._restart_btn: ImageButton = None

		self._size_text: TextString = None
		self._size_display: TextField = None
		self._size_inc_btn: UpArrowButton = None
		self._size_dec_btn: DownArrowButton = None

	def init(self):
		self._screen = pygame.display.get_surface()

	def event(self, event: pygame.event.EventType):
		for ui_element in self._visible_elements:
			ui_element.event(event)

	def step(self, delta: float):
		self._screen.fill(self._back_color)
		for ui_element in self._visible_elements:
			ui_element.render_onto(self._screen)

	def quit(self):
		pass
		
	def _show(self, ui_element: UIElement):
		self._visible_elements.add(ui_element)

	def _hide(self, ui_element: UIElement):
		self._visible_elements.discard(ui_element)

	def _inc_size(self, /):
		new_size = self.size + 1
		if new_size in self._size_range:
			self.size = new_size
		self._update_size_display()

	def _dec_size(self, /):
		new_size = self.size - 1
		if new_size in self._size_range:
			self.size = new_size
		self._update_size_display()


if __name__ == '__main__':
	pygame.init()
	app = App()
	main(app)
	pygame.quit()

