'''\
About properties:
I use a lot of properties to add way to easily extend
the behavior of ui elements, like pre-render.
'''


from typing import Callable

import pygame


class UIElement():

	def __init_subclass__(cls, **kwargs):
		super().__init_subclass__(**kwargs)

	def __init__(self, /, back_color='Ivory', **kwargs):
		super().__init__(**kwargs)
		self.__rect: pygame.Rect = None
		self.__back_color = back_color
		self.__back = True

	def presize(self, rect: pygame.Rect):
		self.__rect = rect

	def event(self, event: pygame.event.EventType):
		pass

	def render_onto(self, surf: pygame.Surface):
		if self.rect is None:
			return
		self._draw_back(surf)

	def _draw_back(self, surf: pygame.Surface):
		if not self.back:
			return
		pygame.draw.rect(surf, self.back_color, self.rect)

	@property
	def rect(self):
		return self.__rect

	@property
	def back_color(self):
		return self.__back_color

	@back_color.setter
	def back_color(self, color):
		self.__back_color = color
		return self.back_color
		
	@property
	def back(self) -> bool:
		return self.__back


class BorderedContainer(UIElement):

	def __init__(self, /, border_radius: int = 0, **kwargs):
		super().__init__(**kwargs)
		self.__content: UIElement = None
		self.__border_radius = border_radius

	def presize(self, rect: pygame.Rect):
		super().presize(rect)
		self._presize_content()

	def render_onto(self, surf: pygame.Surface):
		self._draw_back(surf)
		if self.content is None:
			return
		self.content.render_onto(surf)

	def _draw_back(self, surf: pygame.Surface):
		pygame.draw.rect(
			surf, self.back_color, self.rect,
			border_radius=self.border_radius,
		)

	def _presize_content(self):
		if self.content is None or self.rect is None:
			return
		x = self.rect.x + self.border_radius
		y = self.rect.y + self.border_radius
		width = self.rect.width - 2 * self.border_radius
		height = self.rect.height - 2 * self.border_radius
		self.content.presize(pygame.Rect(x, y, width, height))

	@property
	def content(self):
		return self.__content

	@content.setter
	def content(self, content: UIElement):
		self.__content = content
		return self.content

	@property
	def border_radius(self):
		return self.__border_radius

	@border_radius.setter
	def border_radius(self, radius: int):
		self.__border_radius = radius
		self._presize_content()
		return self.border_radius


class Button(UIElement):
	ON_PRESS = 1
	ON_RELEASE = 2

	def __init__(self, /, **kwargs):
		super().__init__(**kwargs)
		self.__callback = self.__init__
		self.__mode = self.ON_PRESS

	def event(self, event: pygame.event.EventType):
		super().event(event)
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.mouse_act(event.pos, self.ON_PRESS)
		elif event.type == pygame.MOUSEBUTTONUP:
			self.mouse_act(event.pos, self.ON_RELEASE)

	def mouse_act(self, pos, action):
		if self.mode & action:
			self.click_at(pos)

	def click_at(self, pos):
		if self.rect is None:
			return
		if self.rect.collidepoint(pos):
			self.callback(pos)

	@property
	def callback(self):
		return self.__callback

	@callback.setter
	def callback(self, callback: Callable):
		self.__callback = callback
		return self.callback

	@property
	def mode(self):
		return self.__mode

	@mode.setter
	def mode(self, mode: int):
		self.__mode = mode
		return self.mode

