import json

import pygame

from uiboard import UIBoard
from r_ui.text import TextString
from r_ui.timer import Timer, format_ms # fomat minutes seconds
from r_ui.list import VList
from r_ui.particles import ParticlesAnimation
from r_ui.context import Context, ContextSwitcher
from r_ui.advanced import (
	TextField, TextButton,
	UpArrowButton, DownArrowButton,
	ImageButton, ContainerButton,
	LineInput,
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


class RecordsList():

	def __init__(self, size=10):
		self.size = 10
		self.list = []

	def add(self, title: str, size: int, delta: float):
		self.list.append((title, size, delta))
		self.sort()
		self.format()

	def sort(self):
		self.list.sort(key=lambda record: (-record[1], record[2]))

	def format(self):
		if len(self.list) <= self.size:
			return
		last = None
		cnt = 0
		for i, e in enumerate(self):
			if e[1] != last:
				cnt = 0
			cnt += 1
			last = e[1]
			if cnt > 3:
				break
		self.pop(i)

	def download(self, path: str):
		try:
			with open(path) as file:
				new_list = json.load(file)
				if self._is_valid(new_list):
					self.list = new_list
					self.sort()
					self.format()
		except OSError:
			pass # File not found etc.

	def upload(self, path: str):
		try:
			with open(path, 'w') as file:
				json.dump(self.list, file)
		except OSError:
			pass

	def _is_valid(self, data):
		if len(data) / self.size > 2:
			return False
		if not isinstance(data, list):
			return False
		for item in data:
			if len(item) > 3:
				return False
			if not isinstance(item[0], str):
				return False
			if not isinstance(item[1], int):
				return False
			if not isinstance(item[2], float):
				return False
		return True

	def __iter__(self):
		return iter(self.list)


class App():

	def __init__(self):
		# Behavior
		self.size = 3
		self._record_size = self.size # Size of field of the last win
		self._size_range = range(2, 8) # Valid size values
		self._WIN_TEXT = 'WIN!'
		self._records = RecordsList()
		self._records_dump_path = 'records.json'
		# UI details
		self._front_color = 'Ivory'
		self._text_color = 'Black'

		self._screen: pygame.Surface = None
		self._backgroud: pygame.Surface = None
		self._particle_icon: pygame.Surface = None
		self._win_sound: pygame.mixer.Sound = None
		self._click_sound: pygame.mixer.Sound = None

		self._menus: ContextSwitcher = None
		self._game_page: Context = None
		self._main_menu: Context = None
		self._records_page: Context = None
		self._save_record_page: Context = None

		self._to_main_menu_btn: ImageButton = None
		# Main menu
		self._game_title: TextString = None
		self._play_btn: TextButton = None
		self._records_btn: TextButton = None
		# Records page
		self._records_header: TextString = None
		self._records_list: VList = None
		# Save record page
		self._actual_record_view: TextString = None
		self._nickname_input: LineInput = None
		self._save_record_btn: TextButton = None
		# Game page
		self._central_text: TextString = None
		self._win_particles: ParticlesAnimation = None
		# Central text and particles are decorations for win
		self._save_record_after_win_btn: TextButton = None

		self._board: UIBoard = None
		self._board_pad: ContainerButton = None # Make border around board

		self._restart_text: TextButton = None
		self._restart_btn: ImageButton = None

		self._timer: Timer = None

		self._size_text: TextString = None
		self._size_display: TextField = None
		self._size_inc_btn: UpArrowButton = None
		self._size_dec_btn: DownArrowButton = None

	def init(self):
		self._download_records()
		self._screen = pygame.display.get_surface()
		self._background = pygame.image.load('img/back.png').convert()
		self._particle_icon = pygame.image.load('img/particle.png').convert_alpha()
		self._win_sound = pygame.mixer.Sound('sound/win.ogg')
		self._click_sound = pygame.mixer.Sound('sound/click_tick.ogg')

		self._menus = ContextSwitcher()
		self._game_page = Context()
		self._menus.set_context('game', self._game_page)
		self._main_menu = Context()
		self._menus.set_context('menu', self._main_menu)
		self._records_page = Context()
		self._menus.set_context('records', self._records_page)
		self._save_record_page = Context()
		self._menus.set_context('new_record', self._save_record_page)
		self._menus.switch('menu')

		self._to_main_menu_btn = ImageButton(border_radius=5)
		self._to_main_menu_btn.content.src = 'img/back_arrow.png'
		self._to_main_menu_btn.presize(pygame.Rect(30, 2, 26, 26))
		self._to_main_menu_btn.callback = self._go_to_main_menu
		self._game_page.add_elem(self._to_main_menu_btn)
		self._records_page.add_elem(self._to_main_menu_btn)
		self._save_record_page.add_elem(self._to_main_menu_btn)
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
		self._records_btn.presize(pygame.Rect(W // 2 - 60, H // 2 + 35, 120, 30))
		# 5 pixels down the play button
		self._records_btn.content.text = 'Records'
		self._records_btn.callback = self._go_to_records_page
		self._main_menu.add_elem(self._records_btn)
		# Records page
		self._records_header = TextString(text='Records', font='monospace')
		self._records_header.text_color = self._text_color
		self._records_header.presize(pygame.Rect(W // 2 - 100, 20, 200, 40))
		self._records_page.add_elem(self._records_header)

		self._records_list = VList(back=False, spacing=4)
		self._records_list.presize(pygame.Rect(W // 2 - 100, 80, 200, H - 120))
		for _ in range(10):
			self._records_list.append(TextString(
				font='monospace', text_color=self._text_color,
			))
		self._records_page.add_elem(self._records_list)
		# Save record page
		self._nickname_input = LineInput(border_radius=5, line_len=16)
		self._nickname_input.back_color = self._front_color
		self._nickname_input.content.text_color = self._text_color
		self._nickname_input.content.font = 'monospace'
		self._nickname_input.presize(pygame.Rect(W // 2 - 105, 50, 210, 30))
		self._save_record_page.add_elem(self._nickname_input)

		self._actual_record_view = TextString(font='monospace')
		self._actual_record_view.text_color = self._text_color
		self._actual_record_view.presize(pygame.Rect(W // 2, 110, 0, 50))
		self._save_record_page.add_elem(self._actual_record_view)

		self._save_record_btn = TextButton(border_radius=5)
		self._save_record_btn.color = self._front_color
		self._save_record_btn.content.text = 'Save'
		self._save_record_btn.content.font = 'monospace'
		self._save_record_btn.content.text_color = self._text_color
		self._save_record_btn.presize(pygame.Rect(W // 2 - 50, H - 60, 100, 30))
		self._save_record_btn.callback = self._save_new_record
		self._save_record_page.add_elem(self._save_record_btn)
		# Game page
		self._central_text = TextString()
		self._central_text.text_color = self._text_color
		self._central_text.presize(pygame.Rect((0, 0), RESOLUTION))
		self._central_text.font_size = 80
		self._central_text.text = self._WIN_TEXT
		self._game_page.add_elem(self._central_text, layer=+1)
		self._game_page.hide(self._central_text)

		self._win_particles = ParticlesAnimation(image=self._particle_icon)
		self._win_particles.timeout = 10
		self._game_page.add_elem(self._win_particles, layer=2)

		self._board_pad = ContainerButton(border_radius=10)
		self._board_pad.back_color = self._front_color
		self._board = UIBoard()
		self._board.back_color = self._front_color
		self._board_pad.content = self._board
		self._board_pad.presize(pygame.Rect(30, 30, 580, 260))
		self._board_pad.callback = self._check_win
		self._game_page.add_elem(self._board_pad)

		self._restart_text = TextButton(back=False)
		self._restart_text.content.text_color = self._text_color
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

		self._save_record_after_win_btn = TextButton(border_radius=5)
		self._save_record_after_win_btn.content.text_color = self._text_color
		self._save_record_after_win_btn.content.font = 'monospace'
		self._save_record_after_win_btn.content.text = 'Save record'
		self._save_record_after_win_btn.presize(pygame.Rect(410, 310, 200, 30))
		self._save_record_after_win_btn.callback = self._go_to_save_record_page
		self._game_page.add_elem(self._save_record_after_win_btn)
		self._game_page.hide(self._save_record_after_win_btn)

	def event(self, event: pygame.event.EventType):	
		if event.type == pygame.MOUSEBUTTONDOWN:
			self._click_sound.play()
		self._menus.event(event)

	def step(self, delta: float):
		self._screen.blit(self._background, (0, 0))
		self._menus.render_onto(self._screen)

	def quit(self):
		self._upload_records()

	def _download_records(self):
		self._records.download(self._records_dump_path)

	def _upload_records(self):
		self._records.upload(self._records_dump_path)

	def restart(self, *args):
		self._game_page.hide(self._central_text)
		self._game_page.hide(self._save_record_after_win_btn)
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

	def _go_to_save_record_page(self, *args):
		self._menus.switch('new_record')
		self._nickname_input.content.text = 'myrecord'
		self._nickname_input.is_active = True
		self._actual_record_view.text = format_ms(self._timer.get())

	def _finish_pages_progress(self):
		self._timer.stop()

	def _save_new_record(self, *args):
		self._records.add(
			self._nickname_input.get_line(),
			self._record_size,
			self._timer.get(),
		)
		self._records.sort()
		self._go_to_main_menu()

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
		for text_string in self._records_list:
			text_string.text = ''
		for text_string, record in zip(self._records_list, self._records):
			nickname, size, time = record
			text_string.text = f'{nickname: <20}{size: <3}{format_ms(time)}'

	def _check_win(self, *args):
		if self._board.win:
			self._timer.stop()
			self._record_size = self.size
			self._game_page.mute(self._board_pad)
			self._game_page.show(self._save_record_after_win_btn)
			self._game_page.show(self._central_text)
			self._win_particles.restart((W // 2, H // 2))
			self._win_sound.play()

	def _update_size_display(self):
		self._size_display.content.text = str(self.size)


if __name__ == '__main__':
	pygame.init()
	app = App()
	main(app)
	pygame.quit()

