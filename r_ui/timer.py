from time import time

import pygame

from r_ui.text import TextString


class Timer(TextString):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__beg = 0
		self.__end = 0
		self.__is_on = False

	def render_onto(self, surf: pygame.Surface):
		delta = self.get()
		second = delta % 60 // 1
		minute = delta // 60 % 60
		self.text = f'{minute:0> 2}:{second:0> 2}'
		super().render_onto(surf)

	def start(self):
		self.__beg = time()
		self.__is_on = True

	def stop(self):
		self.__is_on = False

	def get(self):
		if self.__is_on:
			self.__end = time()
		return self.__end - self.__beg

