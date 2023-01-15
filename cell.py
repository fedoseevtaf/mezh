'''\
This module contains Cell class.

>>> Cell('tomato', 'cyan', 'orange', 'plum')
Cell(top=tomato, bot=cyan, left=orange, right=plum)
'''


class Cell():

	def __init__(self, top, bot, left, right):
		self.top = top
		self.bot = bot
		self.left = left
		self.right = right

	def __repr__(self) -> str:
		return ('Cell('
			f'top={self.top}, '
			f'bot={self.bot}, '
			f'left={self.left}, '
			f'right={self.right})'
		)


if __name__ == '__main__':
	import doctest
	doctest.testmod()

