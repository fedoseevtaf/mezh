import pygame

from r_ui.base import UIElement


class Text(UIElement):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._text = ''
		self._text_color = 'black'
		self._font_name = 'monospace'
		self._font_type = pygame.font.SysFont
		self._font_size = 0

		self.__font = None
		self.__sufr = None
		self.__rect = None

	def estimate(self):
		if self.__font is None or self.font_type is None:
			return 0, 0
		return self.__font.size(self.text)

	def presize(self, rect):
		self.rect = rect
		self.font_size = self.rect.height

	def render_onto(self, surf):
		self._draw_back(surf)
		if self.__surf is not None:
			surf.blit(self.__surf, self.__rect)

	def _prerender_font(self):
		if self.font_type is None:
			return
		self.__font = self._font_type(self._font_name, self._font_size)

	def _prerender(self):
		if self.__font is None or self.font_type is None:
			return
		self.__surf = self.__font.render(self._text, True, self._text_color)
		self.__rect = self.__surf.get_rect()
		self.__rect.center = self.rect.center

	@property
	def text(self):
		return self._text

	@text.setter
	def text(self, text: str):
		self._text = text
		self._prerender()
		return text

	@property
	def text_color(self):
		return self._text_color

	@text_color.setter
	def text_color(self, color):
		self._text_color = color
		self._prerender()
		return color

	@property
	def font(self):
		return self._font_name

	@font.setter
	def font(self, font: str):
		self._font_name = font
		self._prerender_font()
		self._prerender()
		return font

	@property
	def font_size(self):
		return self._font_size

	@font_size.setter
	def font_size(self, size: int):
		self._font_size = size
		self._prerender_font()
		self._prerender()
		return size

	@property
	def font_type(self):
		return self._font_type

	@font_type.setter
	def font_type(self, font_type):
		self._font_type = font_type
		self._prerender_font()
		self._prerender()
		return font_type

