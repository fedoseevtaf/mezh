'''\
About properties:
I use a lot of properties to add way to easily extend
the behavior of ui elements, like pre-render.
'''


from typing import Callable

import pygame


class UIElement():
	'''\
	Base class for all ui stuff.
	'''

	def __init_subclass__(cls, **kwargs):
		super().__init_subclass__(**kwargs)

	def __init__(self, *args, back_color='Ivory', back=True, **kwargs):
		super().__init__(*args, **kwargs)
		self.__rect: pygame.Rect = None # Place of the ui element
		self.__back_color = back_color
		self.__back = back # Draw background or not

	def presize(self, rect: pygame.Rect):
		'''\
		To draw ui element you need to set it's place.
		'''

		self.__rect = rect

	def event(self, event: pygame.event.EventType):
		'''\
		ALL events should be send to that method
		to make ui element 'alive'.
		'''

		pass

	def render_onto(self, surf: pygame.Surface):
		'''\
		Draw the ui element to the surface. Surface is independent
		by the ui element.
		'''

		if self.rect is None:
			return
		self._draw_back(surf)

	def _draw_back(self, surf: pygame.Surface):
		if not self.back:
			return
		pygame.draw.rect(surf, self.back_color, self.rect)

	@property
	def rect(self):
		'''\
		You can't set it: use 'presize' method.
		'''

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

	@back.setter
	def back(self, back: bool):
		self.__back = back
		return self.back


class BorderedContainer(UIElement):
	'''\
	Provide shell for the 'content' ui element
	and make back with border radius.
	'''

	def __init__(self, *args, border_radius: int = 0, **kwargs):
		super().__init__(*args, **kwargs)
		self.__content: UIElement = None
		self.__border_radius = border_radius

	def presize(self, rect: pygame.Rect):
		'''\
		Presize content ui element considering the border radius.
		'''

		super().presize(rect)
		self._presize_content()
		
	def event(self, event: pygame.event.EventType):
		'''\
		Throw events to the content.
		'''

		super().event(event)
		if self.content is None:
			return
		self.content.event(event)

	def render_onto(self, surf: pygame.Surface):
		'''\
		Draw back with border radius and content over it.
		'''

		self._draw_back(surf)
		if self.content is None:
			return
		self.content.render_onto(surf)

	def _draw_back(self, surf: pygame.Surface):
		if not self.back:
			return
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
	'''\
	Simple class to make interactive ui elements
	for mouse actions.
	'''

	ON_PRESS = 1
	ON_RELEASE = 2

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__callback = print
		self.__mode = self.ON_PRESS

	def event(self, event: pygame.event.EventType):
		'''\
		Event handling and defining mode of action.
		'''

		super().event(event)
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.mouse_act(event.pos, self.ON_PRESS)
		elif event.type == pygame.MOUSEBUTTONUP:
			self.mouse_act(event.pos, self.ON_RELEASE)

	def mouse_act(self, pos, action):
		'''\
		Handling mode of action.
		'''

		if self.mode & action:
			self.click_at(pos)

	def click_at(self, pos):
		'''\
		Check that mouse action is on the button.
		'''

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

