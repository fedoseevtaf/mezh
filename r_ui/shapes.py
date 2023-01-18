import pygame

from r_ui.base import UIElement


class Shape(UIElement):
	'''
	UI element without purpose just with draw method.
	'''

	def __init__(self, *args, color='Sienna', **kwargs):
		super().__init__(*args, **kwargs)
		self.__color = color # Simple property for base color of shape

	@property
	def color(self):
		return self.__color

	@color.setter
	def color(self, color):
		self.__color = color
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
				self.rect.midbottom,
				self.rect.topleft,
				self.rect.topright,
			)
		)

