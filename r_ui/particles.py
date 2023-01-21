from random import random
from time import time

import pygame

from r_ui.base import UIElement


class _Particle(pygame.sprite.Sprite):

	def __init__(self, *args, image: pygame.Surface, Vx, Vy):
		super().__init__()
		self.image = image
		self.rect = image.get_rect()
		self.Vx = Vx
		self.Vy = Vy # Base velocity on restart
		self.Vy_t = Vy # Actual velocity at time

	def update(self, *args, restart=False, dt=0, g=10, pos=(0, 0)):
		if restart:
			self.rect.center = pos
			self.Vy_t = self.Vy
		else:
			self.rect.x += self.Vx * dt
			self.rect.y += self.Vy_t * dt
			self.Vy_t += g * dt


class ParticlesAnimation(UIElement):

	def __init__(self, *args, image: pygame.Surface, number: int = 300, **kwargs):
		super().__init__(*args, **kwargs)
		self.__particles = pygame.sprite.Group(*(
			_Particle(image=image, Vx=random() * 20 - 10, Vy=random() * 20 - 17)
			for _ in range(number)
		))
		self.__timeout = 0
		self.__start = 0

	def restart(self, pos):
		self.__particles.update(restart=True, pos=pos)
		self.__start = time()

	def render_onto(self, surf: pygame.Surface):
		dt = time() - self.__start
		if dt > self.timeout:
			return
		self.__particles.update(dt=dt, g=0.2)
		self.__particles.draw(surf)

	@property
	def timeout(self) -> float:
		return self.__timeout

	@timeout.setter
	def timeout(self, timeout: float):
		self.__timeout = timeout
		return self.timeout

