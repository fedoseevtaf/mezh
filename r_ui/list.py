from typing import List

import pygame

from r_ui.base import UIElement


class UIList(UIElement):

	def __init__(self, *args, spacing=0, **kwargs):
		super().__init__(*args, **kwargs)
		self.__spacing = spacing
		self.__items: List[UIElement] = []

	def presize(self, rect: pygame.Rect):
		super().presize(rect)
		self._presize_items()

	def render_onto(self, surf: pygame.Surface):
		super().render_onto(surf)
		for ui_element in self:
			ui_element.render_onto(surf)

	def event(self, event: pygame.event.EventType):
		super().event(event)
		for ui_element in self:
			ui_element.event(event)

	def append(self, ui_element: UIElement):
		self.__items.append(ui_element)
		self._presize_items()

	def popitem(self) -> UIElement:
		if self.__items:
			return self.pop()
			self._presize_items()
	
	def __len__(self) -> int:
		return len(self.__items)

	def __iter__(self):
		return iter(self.__items)

	def _presize_items(self):
		pass

	@property
	def spacing(self) -> int:
		return self.__spacing

	@spacing.setter
	def spacing(self, spacing: int):
		self.__spacing = spacing
		return self.spacing


class VList(UIList):

	def _presize_items(self):
		if self.rect is None:
			return
		if not len(self):
			return
		x = self.rect.x
		width = self.rect.width
		y = self.rect.y
		height = (self.rect.height - self.spacing * (len(self) - 1)) // (len(self))
		for ui_element in self:
			ui_element.presize(pygame.Rect(x, y, width, height))
			y += height + self.spacing

