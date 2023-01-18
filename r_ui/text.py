import pygame

from r_ui.base import UIElement


class TextString(UIElement):
	'''\
	Class for single line of text with no background.
	'''

	def __init__(self, *args, 
			text: str = '', font: str = 'monospace',
			text_color='black', **kwargs):
		super().__init__(*args, **kwargs)
		self.__text = text
		self.__text_color = text_color
		# You can use pygame.font.Font or pygame.freetype.Font
		# instead of pygame.font.Sysfont to use custom font
		# (font type)
		# And 'path/of.font' as font name
		self.__font_name = font
		self.__font_type = pygame.font.SysFont
		self.__font_size = 0

		self.__font = None
		self.__sufr = None
		self.__text_rect = None

	def estimate(self):
		'''\
		Help you estimate size of text string
		while you place ui elements.
		'''

		if self.__font is None:
			return 0, 0
		return self.__font.size(self.text)

	def presize(self, rect):
		super().presize(rect)
		self.font_size = self.rect.height

	def render_onto(self, surf):
		if self.__surf is not None:
			surf.blit(self.__surf, self.__text_rect)

	def _prerender_font(self):
		if self.font_type is None:
			return
		self.__font = self.font_type(self.font, self.font_size)

	def _prerender(self):
		if self.__font is None:
			return
		self.__surf = self.__font.render(self.text, True, self.text_color)
		self.__text_rect = self.__surf.get_rect()
		if self.rect is None:
			return
		self.__text_rect.center = self.rect.center

	@property
	def text(self):
		return self.__text

	@text.setter
	def text(self, text: str):
		self.__text = text
		self._prerender()
		return text

	@property
	def text_color(self):
		return self.__text_color

	@text_color.setter
	def text_color(self, color):
		self.__text_color = color
		self._prerender()
		return color

	@property
	def font(self):
		return self.__font_name

	@font.setter
	def font(self, font: str):
		self.__font_name = font
		self._prerender_font()
		self._prerender()
		return font

	@property
	def font_size(self):
		return self.__font_size

	@font_size.setter
	def font_size(self, size: int):
		self.__font_size = size
		self._prerender_font()
		self._prerender()
		return size

	@property
	def font_type(self):
		return self.__font_type

	@font_type.setter
	def font_type(self, font_type):
		self.__font_type = font_type
		self._prerender_font()
		self._prerender()
		return font_type

