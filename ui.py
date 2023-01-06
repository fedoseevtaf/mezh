import pygame


class UIElement():

	def __init_subclass__(cls, **kwargs):
		super().__init_subclass__(**kwargs)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rect = None
		self.back_color = 'Ivory'

	def presize(self, rect):
		self.rect = rect

	def render_onto(self, surf):
		if self.rect is None:
			return
		self._draw_back(surf)

	def _draw_back(self, surf):
		pygame.draw.rect(surf, self.back_color, self.rect)


class Button(UIElement):
	ON_PRESS = 1
	ON_RELEASE = 2

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.callback = self.__init__
		self.mode = self.ON_PRESS

	def event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.mouse_act(event.pos, self.ON_PRESS)
		elif event.type == pygame.MOUSEBUTTONUP:
			self.mouse_act(event.pos, self.ON_RELEASE)

	def mouse_act(self, pos, action):
		if self.mode & action:
			self.click_at(pos)

	def click_at(self, pos):
		if self.rect.colidepoint(pos):
			self.callback(pos)


class Text(UIElement):

	def __init__(self, *args, **kwargs):
		super().__init__(self)
		self._text = ''
		self._text_color = 'black'
		self._font_name = 'monospace'
		self._font_size = 0

		self._prerender_sufr = None
		self._prerender_rect = None

	def presize(self, rect):
		self.rect = rect
		self.font_size = self.rect.height

	def render_onto(self, surf):
		self._draw_back(surf)
		surf.blit.






