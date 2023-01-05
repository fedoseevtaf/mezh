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


class Field():

	def __init__(self):
		self.width = 0
		self.height = 0
		self._field = {}

	def resize(self, width: int, height: int):
		self.width = width
		self.height = height
		self._field.clear()
		for row in range(height):
			for col in range(width):
				self._field[row, col] = NoCell()

	def get_at(self, row: int, col: int) -> Cell:
		if not (0 <= row < self.height):
			return NoCell()
		if not (0 <= col < self.width):
			return NoCell()
		return self._field[row, col]

	def set_at(self, row: int, col: int, cell: Cell) -> Cell:
		previous = self.get_at(row, col)
		self._field[row, col] = cell
		return previous

	def canset(self, row: int, col: int, cell: Cell) -> bool:
		return (
			self.get_at(row - 1, col).bot == cell.top and
			self.get_at(row + 1, col).top == cell.bot and
			self.get_at(row, col - 1).right == cell.left and
			self.get_at(row, col + 1).left == cell.right
		)

	def _row_matching(self):
		for row in range(self.height):
			for col in range(1, self.width):
				cell = self.get_at(row, col)
				last_cell = self.get_at(row, col - 1)
				yield last_cell.right == cell.left

	def _col_matching(self):
		for col in range(self.width):
			for row in range(1, self.height):
				cell = self.get_at(row, col)
				last_cell = self.get_at(row - 1, col)
				yield last_cell.bot == cell.top

	def ismatched(self) -> bool:
		if NoCell() in self._field.values():
			return False
		return all(self._row_matching()) and all(self._col_matching())

