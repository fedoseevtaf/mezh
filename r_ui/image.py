import pygame

from r_ui.base import UIElement


class Image(UIElement):

	def __init__(self, /, src: str = None, **kwargs):
		super().__init__(**kwargs)
		self.__src = src
		self.__image_rect = None
		self.__origin = None
		self.__surf = None
		
	def presize(self, rect):
		super().presize(rect)
		self._prerender()
		
	def render_onto(self, surf):
		if self.__surf is not None:
			surf.blit(self.__surf, self.__image_rect)
		
	def _load(self):
		self.__origin = pygame.image.load(self.__src).convert_alpha()
		
	def _prerender(self):
		if self.__src is None:
			return
		if self.__origin is None:
			self._load()
		self.__surf = pygame.transform.scale(self.__origin, self.rect.size)
		self.__image_rect = self.__surf.get_rect()
		self.__image_rect.center = self.rect.center
		
	@property
	def src(self):
		return self.__src
		
	@src.setter
	def src(self, src: str):
		self.__src = src
		self._prerender()
		return self.src

