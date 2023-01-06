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


class BorderedContainer(UIElement):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.content: UIElement = None
		self._border_radius = 0

	def presize(self, rect):
		self.rect = rect
		self._presize_content()

	def render_onto(self, surf):
		self._draw_back(surf)
		if self.content is None:
			return
		self.content.render_onto(surf)

	def _draw_back(self, surf):
		pygame.draw.rect(
			surf, self.rect, self.back_color,
			border_radius=self.border_radius,
		)

	def _presize_content(self):
		x = self.rect.x + self.border_radius
		y = self.rect.y + self.border_radius
		width = self.rect.width - 2 * self.border_radius
		height = self.rect.height - 2 * self.border_radius
		self.content.presize(pygame.Rect(x, y, width, height))

	@property
	def border_radius(self):
		return self._border_radius

	@border_radius.setter
	def border_radius(self, radius: int):
		self._border_radius = radius
		self._presize_content()
		return radius


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

