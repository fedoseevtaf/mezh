from r_ui.base import UIElement, BorderedContainer, Button
from r_ui.text import Text
from r_ui.shapes import UpTriangle, DownTriangle


class ContainerButton(Button, BorderedContainer):
	pass


class BorderedContent(BorderedContainer):

	def __init_subclass__(cls, content_type=None, **kwargs):
		super().__init_subclass__()
		cls.__content = content_type

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.__content is None:
			return
		self.__content = self.__content()

	@property
	def content(self):
		return self._content

	@content.setter
	def content(self, content):
		return


class TextField(BorderedContent, content_type=Text):
	pass


class TextButton(Button, BorderedContent, content_type=Text):
	pass


class UpArrowButton(Button, BorderedContent, content_type=UpTriangle):
	pass


class DownArrowButton(Button, BorderedContent, content_type=DownTriangle):
	pass

