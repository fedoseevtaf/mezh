from typing import Set

import pygame

from uiboard import UIBoard
from r_ui.base import UIElement
from r_ui.text import TextString
from r_ui.advanced import (
	TextField, TextButton,
	UpArrowButton, DownArrowButton,
	ImageButton, ContainerButton,
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
		self._board_pad: ContainerButton = None

		self._restart_text: TextButton = None
		self._restart_btn: ImageButton = None

		self._size_text: TextString = None
		self._size_display: TextField = None
		self._size_inc_btn: UpArrowButton = None
		self._size_dec_btn: DownArrowButton = None

	def init(self):
		self._central_text = TextString()
		self._central_text.text_color = self._text_color
		self._central_text.presize(pygame.Rect((0, 0), RESOLUTION))
		self._show(self._central_text)

		self._screen = pygame.display.get_surface()
		self._board_pad = ContainerButton(border_radius=10)
		self._board_pad.back_color = self._front_color
		self._board = UIBoard()
		self._board.back_color = self._front_color
		self._board_pad.content = self._board
		self._board_pad.presize(pygame.Rect(30, 30, 580, 260))
		self._board_pad.callback = self._check_win
		self._show(self._board_pad)

		self._restart_text = TextButton()
		self._restart_text.back_color = self._back_color
		self._restart_text.content.font = 'monospace'
		self._restart_text.content.text = 'Restart'
		self._restart_text.presize(pygame.Rect(30, 310, 130, 30))
		self._restart_text.callback = self.restart
		self._show(self._restart_text)

		self._restart_btn = ImageButton(border_radius=5)
		self._restart_btn.back_color = self._front_color
		self._restart_btn.content.src = 'img/restart_icon.png'
		self._restart_btn.presize(pygame.Rect(160, 310, 30, 30))
		self._restart_btn.callback = self.restart
		self._show(self._restart_btn)

		self._size_text = TextString(text='Size', font='monospace')
		self._size_text.presize(pygame.Rect(210, 310, 80, 30))
		self._show(self._size_text)

		self._size_display = TextField(border_radius=5)
		self._size_display.back_color = self._front_color
		self._size_display.presize(pygame.Rect(290, 310, 30, 30))
		self._size_display.content.font = 'monospace'
		self._update_size_display()
		self._show(self._size_display)

		self._size_inc_btn = UpArrowButton(border_radius=3)
		self._size_inc_btn.presize(pygame.Rect(325, 310, 25, 14))
		self._size_inc_btn.callback = self._inc_size
		self._show(self._size_inc_btn)

		self._size_dec_btn = DownArrowButton(border_radius=3)
		self._size_dec_btn.presize(pygame.Rect(325, 326, 25, 14))
		self._size_dec_btn.callback = self._dec_size
		self._show(self._size_dec_btn)

		self.restart()

	def event(self, event: pygame.event.EventType):
		for ui_element in frozenset(self._visible_elements):
			ui_element.event(event)

	def step(self, delta: float):
		self._screen.fill(self._back_color)
		for ui_element in self._visible_elements:
			ui_element.render_onto(self._screen)

	def quit(self):
		pass

	def restart(self, *args):
		self._central_text.text = ''
		self._board.resize(self.size, self.size)
		self._board.restart()
		self._show(self._board_pad)
		
	def _show(self, ui_element: UIElement):
		self._visible_elements.add(ui_element)

	def _hide(self, ui_element: UIElement):
		self._visible_elements.discard(ui_element)

	def _inc_size(self, *args):
		new_size = self.size + 1
		if new_size in self._size_range:
			self.size = new_size
		self._update_size_display()

	def _dec_size(self, *args):
		new_size = self.size - 1
		if new_size in self._size_range:
			self.size = new_size
		self._update_size_display()

	def _check_win(self, *args):
		if self._board.win:
			self._central_text.font_size = 80
			self._central_text.text = self._WIN_TEXT

	def _update_size_display(self):
		self._size_display.content.text = str(self.size)


if __name__ == '__main__':
	pygame.init()
	app = App()
	main(app)
	pygame.quit()

