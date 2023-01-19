import pygame

from uiboard import UIBoard
from r_ui.text import TextString
from r_ui.timer import Timer
from r_ui.context import Context, ContextSwitcher
from r_ui.input import KeyInput
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
		self._size_range = range(2, 8)
		self._WIN_TEXT = 'WIN!'
		# UI details
		self._screen: pygame.Surface = None
		self._backgroud: pygame.Surface = None
		self._win_sound: pygame.mixer.Sound = None

		self._front_color = 'Ivory'
		self._text_color = 'Black'

		self._menus: ContextSwitcher = None
		self._game_page: Context = None
		self._main_menu: Context = None
		self._records_page: Context = None
		
		self._to_main_menu_btn: ImageButton = None
		# Main menu
		self._game_title: TextString = None
		self._play_btn: TextButton = None
		self._records_btn: TextButton = None
		# Game page
		self._central_text: TextString = None

		self._board: UIBoard = None
		self._board_pad: ContainerButton = None

		self._restart_text: TextButton = None
		self._restart_btn: ImageButton = None

		self._timer: Timer = None

		self._size_text: TextString = None
		self._size_display: TextField = None
		self._size_inc_btn: UpArrowButton = None
		self._size_dec_btn: DownArrowButton = None

	def init(self):
		self._screen = pygame.display.get_surface()
		self._background = pygame.image.load('img/back.png').convert()
		self._win_sound = pygame.mixer.Sound('sound/win.ogg')

		self._menus = ContextSwitcher()
		self._game_page = Context()
		self._menus.set_context('game', self._game_page)
		self._main_menu = Context()
		self._menus.set_context('menu', self._main_menu)
		self._records_page = Context()
		self._menus.set_context('records', self._records_page)
		self._menus.switch('menu')

		self._to_main_menu_btn = ImageButton(border_radius=5)
		self._to_main_menu_btn.content.src = 'img/back_arrow.png'
		self._to_main_menu_btn.presize(pygame.Rect(30, 2, 26, 26))
		self._to_main_menu_btn.callback = self._go_to_main_menu
		self._game_page.add_elem(self._to_main_menu_btn)
		self._records_page.add_elem(self._to_main_menu_btn)
		# Main menu
		self._game_title = TextString(text='Mezh Tetravex', font='monospace')
		self._game_title.text_color = self._text_color
		self._game_title.presize(pygame.Rect(0, 0, W, H // 2))
		self._game_title.font_size = 65
		self._main_menu.add_elem(self._game_title)

		self._play_btn = TextButton(border_radius=5)
		self._play_btn.presize(pygame.Rect(W // 2 - 60, H // 2, 120, 30))
		self._play_btn.content.text = 'Play'
		self._play_btn.callback = self._go_to_game_page
		self._main_menu.add_elem(self._play_btn)

		self._records_btn = TextButton(border_radius=5)
		# 5 pixels down the play button
		self._records_btn.presize(pygame.Rect(W // 2 - 60, H // 2 + 35, 120, 30))
		self._records_btn.content.text = 'Records'
		self._records_btn.callback = self._go_to_records_page
		self._main_menu.add_elem(self._records_btn)
		# Records page
		self._nickname_input = KeyInput()
		self._nickname_input.is_active = True
		self._records_page.add_elem(self._nickname_input)
		# Game page
		self._central_text = TextString()
		self._central_text.text_color = self._text_color
		self._central_text.presize(pygame.Rect((0, 0), RESOLUTION))
		self._game_page.add_elem(self._central_text, layer=+1)

		self._board_pad = ContainerButton(border_radius=10)
		self._board_pad.back_color = self._front_color
		self._board = UIBoard()
		self._board.back_color = self._front_color
		self._board_pad.content = self._board
		self._board_pad.presize(pygame.Rect(30, 30, 580, 260))
		self._board_pad.callback = self._check_win
		self._game_page.add_elem(self._board_pad)

		self._restart_text = TextButton(back=False)
		self._restart_text.content.font = 'monospace'
		self._restart_text.content.text = 'Restart'
		self._restart_text.presize(pygame.Rect(30, 310, 130, 30))
		self._restart_text.callback = self.restart
		self._game_page.add_elem(self._restart_text)

		self._restart_btn = ImageButton(border_radius=5)
		self._restart_btn.back_color = self._front_color
		self._restart_btn.content.src = 'img/restart_icon.png'
		self._restart_btn.presize(pygame.Rect(160, 310, 30, 30))
		self._restart_btn.callback = self.restart
		self._game_page.add_elem(self._restart_btn)

		self._timer = Timer(text='00:00', font='monospace')
		self._timer.text_color = self._text_color
		self._timer.presize(pygame.Rect(520, 0, 90, 30))
		self._game_page.add_elem(self._timer)

		self._size_text = TextString(text='Size', font='monospace')
		self._size_text.presize(pygame.Rect(210, 310, 80, 30))
		self._game_page.add_elem(self._size_text)

		self._size_display = TextField(border_radius=5)
		self._size_display.back_color = self._front_color
		self._size_display.presize(pygame.Rect(290, 310, 30, 30))
		self._size_display.content.font = 'monospace'
		self._update_size_display()
		self._game_page.add_elem(self._size_display)

		self._size_inc_btn = UpArrowButton(border_radius=3)
		self._size_inc_btn.presize(pygame.Rect(325, 310, 25, 14))
		self._size_inc_btn.callback = self._inc_size
		self._game_page.add_elem(self._size_inc_btn)

		self._size_dec_btn = DownArrowButton(border_radius=3)
		self._size_dec_btn.presize(pygame.Rect(325, 326, 25, 14))
		self._size_dec_btn.callback = self._dec_size
		self._game_page.add_elem(self._size_dec_btn)

	def event(self, event: pygame.event.EventType):
		self._menus.event(event)

	def step(self, delta: float):
		self._screen.blit(self._background, (0, 0))
		self._menus.render_onto(self._screen)

	def quit(self):
		pass

	def restart(self, *args):
		self._central_text.text = ''
		self._board.resize(self.size, self.size)
		self._board.restart()
		self._game_page.loud(self._board_pad)
		self._timer.start()

	def _go_to_game_page(self, *args):
		self._menus.switch('game')
		self.restart()

	def _go_to_main_menu(self, *args):
		self._menus.switch('menu')
		self._finish_pages_progress()

	def _go_to_records_page(self, *args):
		self._menus.switch('records')
		self._update_records()

	def _finish_pages_progress(self):
		self._timer.stop()

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

	def _update_records(self):
		pass

	def _check_win(self, *args):
		if self._board.win:
			self._timer.stop()
			self._game_page.mute(self._board_pad)
			self._central_text.font_size = 80
			self._central_text.text = self._WIN_TEXT
			self._win_sound.play()

	def _update_size_display(self):
		self._size_display.content.text = str(self.size)


if __name__ == '__main__':
	pygame.init()
	app = App()
	main(app)
	pygame.quit()

