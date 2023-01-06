import pygame

from board import Board
from field import NoCell

from r_ui.base import UIElement


class UIBoard(UIElement, Board):

	def __init__(self):
		super().__init__()
		self.rect = None
		self.side = None

		self.outline_color = 'Gray'
		self.outline_width = 2

	def presize(self, rect):
		self.rect = rect
		self._calc_side()

	def _calc_side(self):
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
			self._draw_cell(surf, rect, cell)

	def _draw_buff_field(self, surf):
		rect = pygame.Rect(0, 0, self.side, self.side)
		for point in self._points_of(self._buff_field):
			rect.x = self.rect.right - (point[1] + 1) * self.side
			rect.y = self.rect.y + point[0] * self.side
			cell = self._buff_field.get_at(*point)
			self._draw_cell(surf, rect, cell)

	def _draw_cell(self, surf, rect, cell):
		if isinstance(cell, NoCell):
			return self._draw_cell_outline(surf, rect)
		pygame.draw.polygon(surf, cell.top, (rect.center,
							rect.topleft, rect.topright))
		pygame.draw.polygon(surf, cell.left, (rect.center,
							rect.topleft, rect.bottomleft))
		pygame.draw.polygon(surf, cell.bot, (rect.center,
							rect.bottomleft, rect.bottomright))
		pygame.draw.polygon(surf, cell.right, (rect.center,
							rect.topright, rect.bottomright))
		self._draw_cell_outline(surf, rect)

	def _draw_cell_outline(self, surf, rect):
		pygame.draw.rect(surf, self.outline_color, rect, width=1)










