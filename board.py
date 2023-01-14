import random

from cell import Cell
from field import Field


COLORS = (
	'Crimson', 'MediumVioletRed',
	'DarkOrange', 'Gold',
	'BlueViolet', 'YellowGreen',
	'MediumSlateBlue', 'Chocolate',
	'Ivory', 'Black',
)


def color_map(width: int, height: int) -> dict:
	matrix = {}
	for row in range(height):
		for col in range(width):
			matrix[row, col] = random.choice(COLORS)
	return matrix


class Board():

	def __init__(self):
		self._fields = {
			'main': Field(),
			'buff': Field(),
		}

	@property
	def _main_field(self) -> Field:
		return self._fields['main']

	@property
	def _buff_field(self) -> Field:
		return self._fields['buff']

	@property
	def win(self) -> bool:
		return self._main_field.ismatched()

	def resize(self, width: int, height: int):
		self._main_field.resize(width, height)
		self._buff_field.resize(width, height)

	def restart(self):
		v_map, h_map = self._create_color_maps()
		points = tuple(self._points_of(self._main_field))
		k = self._main_field.width * self._main_field.height
		for rand_point, point in zip(random.sample(points, k), points):
			cell = self._painted_cell(v_map, h_map, point)
			self._buff_field.set_at(*rand_point, cell)

	def _points_of(self, field: Field):
		for row in range(field.height):
			for col in range(field.width):
				yield row, col

	def _painted_cell(self, v_map, h_map, point):
		row, col = point
		return Cell(
			v_map[row, col], v_map[row + 1, col],
			h_map[row, col], h_map[row, col + 1],
		)

	def _create_color_maps(self):
		width = self._main_field.width
		height = self._main_field.height
		yield color_map(width, height + 1)
		yield color_map(width + 1, height)

	def move(
			self,
			field_1, row_1: int, col_1: int,
			field_2, row_2: int, col_2: int,
		):
		if field_1 not in self._fields:
			return
		if field_2 not in self._fields:
			return
		field_1 = self._fields[field_1]
		field_2 = self._fields[field_2]
		self._move(field_1, row_1, col_1, field_2, row_2, col_2)

	def _move(
			self,
			field_1: Field, row_1: int, col_1: int,
			field_2: Field, row_2: int, col_2: int
		):
		actual_1 = field_1.get_at(row_1, col_1)
		actual_2 = field_2.get_at(row_2, col_2)
		field_1.set_at(row_1, col_1, actual_2)
		field_2.set_at(row_2, col_2, actual_1)

