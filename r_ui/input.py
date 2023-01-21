import pygame

from r_ui.base import UIElement


class KeyInput(UIElement):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__is_active = False

	def event(self, event: pygame.event.EventType):
		super().event(event)
		if not self.is_active:
			return
		if event.type == pygame.KEYDOWN:
			# K_RETURN is Enter
			if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
				self.is_active = False
			elif event.key == pygame.K_BACKSPACE:
				self.del_char()
			else:
				self.new_char(event.unicode)

	def new_char(self, char: str):
		print(char)

	def get_line(self) -> str:
		return ''

	@property
	def is_active(self) -> bool:
		return self.__is_active

	@is_active.setter
	def is_active(self, mode: bool):
		self.__is_active = mode
		return self.is_active

