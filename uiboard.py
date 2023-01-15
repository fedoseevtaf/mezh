from math import sin
from time import time

import pygame

from board import Board
from field import NoCell
from r_ui.base import Button


class UIBoard(Button, Board):

	def __init__(self):
		super().__init__()
		self.side = 0
		self.pad_color = 'LightGray'
		self._focus = None
		
	def callback(self, pos):
		if self.rect is None:
			return
		board, cell = self.find_cell(pos)
		if board is None:
			return
		if self._focus is None:
			self._focus = board, cell
			return
		self.move(self._focus[0], *self._focus[1], board, *cell)
		self._focus = None
		
	def find_cell(self, pos):
		on_main = self._find_cell_on_main(pos)
		on_buff = self._find_cell_on_buff(pos)
		if on_main is not None:
			yield 'main'
			yield on_main
		elif on_buff is not None:
			yield 'buff'
			yield on_buff
		else:
			yield None
			yield None
			
	def restart(self):
		super().restart()
		self._calc_side()

	def presize(self, rect):
		super().presize(rect)
		self._calc_side()

	def _calc_side(self):
		if self._main_field.width == 0:
			return
		total_width = self._main_field.width + 1 + self._buff_field.width
		total_height = max(self._main_field.height, self._buff_field.height)

		xside = self.rect.width // total_width
		yside = self.rect.height // total_height
		self.side = min(xside, yside)

	def render_onto(self, surf):
		if self.rect is None:
			return
		self._draw_back(surf)
		self._draw_main_field(surf)
		self._draw_buff_field(surf)

	def _draw_main_field(self, surf):
		rect = pygame.Rect(0, 0, self.side, self.side)
		for point in self._points_of(self._main_field):
			rect.x = self.rect.x + point[1] * self.side
			rect.y = self.rect.y + point[0] * self.side
			cell = self._main_field.get_at(*point)
			self._draw_cell_pad(surf, rect)
			self._draw_cell(surf, rect, cell)
			self._draw_cell_focus(surf, rect, point, 'main')

	def _draw_buff_field(self, surf):
		rect = pygame.Rect(0, 0, self.side, self.side)
		for point in self._points_of(self._buff_field):
			rect.x = self.rect.right - (self._buff_field.width - point[1]) * self.side
			rect.y = self.rect.y + point[0] * self.side
			cell = self._buff_field.get_at(*point)
			self._draw_cell_pad(surf, rect)
			self._draw_cell(surf, rect, cell)
			self._draw_cell_focus(surf, rect, point, 'buff')

	def _draw_cell(self, surf, rect, cell):
		if isinstance(cell, NoCell):
			return
		pygame.draw.polygon(surf, cell.top, (rect.center,
							rect.topleft, rect.topright))
		pygame.draw.polygon(surf, cell.left, (rect.center,
							rect.topleft, rect.bottomleft))
		pygame.draw.polygon(surf, cell.bot, (rect.center,
							rect.bottomleft, rect.bottomright))
		pygame.draw.polygon(surf, cell.right, (rect.center,
							rect.topright, rect.bottomright))
							
	def _draw_cell_focus(self, surf, rect, point, board):
		if self._focus is None or self._focus[0] != board or self._focus[1] != point:
			return
		focus_rect = rect.copy()
		focus_rect.width *= 0.8
		focus_rect.height *= 0.8
		focus_rect.center = rect.center
		pygame.draw.ellipse(surf, self._get_focus_color(), focus_rect, width=3)
	
	def _draw_cell_pad(self, surf, rect):
		pad_rect = rect.copy()
		pad_rect.width *= 0.8
		pad_rect.height *= 0.8
		pad_rect.center = rect.center
		pygame.draw.ellipse(surf, self.pad_color, pad_rect)
		
	def _find_cell_on_main(self, pos):
		row = (pos[1] - self.rect.y) // self.side
		col = (pos[0] - self.rect.x) // self.side
		if row not in range(self._main_field.height):
			return
		if col not in range(self._main_field.width):
			return
		return row, col
		
	def _get_focus_color(self):
		t = time()
		return (
			abs(int(sin(t) * 255)),
			abs(int(sin(t + 2) * 255)),
			abs(int(sin(t * 2) * 255)),
		)
		
	def _find_cell_on_buff(self, pos):
		row = (pos[1] - self.rect.y) // self.side
		col = (pos[0] - self.rect.right) // self.side
		col += self._buff_field.width
		if row not in range(self._buff_field.height):
			return
		if col not in range(self._buff_field.width):
			return
		return row, col

