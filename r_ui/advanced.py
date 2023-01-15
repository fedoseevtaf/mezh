from r_ui.base import BorderedContainer, Button
from r_ui.text import TextString
from r_ui.image import Image
from r_ui.shapes import UpTriangle, DownTriangle


class ContainerButton(Button, BorderedContainer):
	pass


class BorderedContent(BorderedContainer):

	def __init_subclass__(cls, content_type=None, **kwargs):
		super().__init_subclass__(**kwargs)
		cls.__content = content_type

	def __init__(self, /, **kwargs):
		super().__init__(**kwargs)
		if self.__content is None:
			return
		self.__content = self.__content()

	@property
	def content(self):
		return self.__content

	@content.setter
	def content(self, content):
		return self.content


class TextField(BorderedContent, content_type=TextString):
	pass


class TextButton(Button, BorderedContent, content_type=TextString):
	pass


class UpArrowButton(Button, BorderedContent, content_type=UpTriangle):
	pass


class DownArrowButton(Button, BorderedContent, content_type=DownTriangle):
	pass


class ImageButton(Button, BorderedContent, content_type=Image):
	pass

