import pygame

from r_ui.base import UIElement


class Shape(UIElement):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._color = 'black'

	@property
	def color(self):
		return self._color

	@color.setter
	def color(self, color):
		self._color = color
		return color


class UpTriangle(Shape):

	def render_onto(self, surf):
		pygame.draw.polygon(
			surf, self.color, (
				self.rect.midtop,
				self.rect.bottomleft,
				self.rect.bottomright,
			)
		)


class DownTriangle(Shape):

	def render_onto(self, surf):
		pygame.draw.polygon(
			surf, self.color, (
				self.midbottom,
				self.topleft,
				self.topright,
			)
		)










