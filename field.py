from cell import Cell


class NoCell():
	__instance = None

	def __new__(cls) -> object:
		if cls.__instance is None:
			cls.__instance = super().__new__(cls)
		return cls.__instance

	def __init__(self):
		self.top = None
		self.bot = None
		self.left = None
		self.right = None


