from r_ui.base import BorderedContainer, Button
from r_ui.text import TextString
from r_ui.image import Image
from r_ui.input import KeyInput
from r_ui.shapes import UpTriangle, DownTriangle


class ContainerButton(Button, BorderedContainer):
	'''\
	Just button with border radius,
	but it can be used as a 'smart' bordered container.
	'''

	pass


class BorderedContent(BorderedContainer):
	'''\
	It is a bordered container with no way to change content.
	Instead content type is presetted by the class constructor with
	inheritance of this class.
	'''

	def __init_subclass__(cls, content_type=None, **kwargs):
		super().__init_subclass__(**kwargs)
		cls.__content = content_type

	def __init__(self, *args, **kwargs):
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
	'''\
	Text with border radius on back.
	Use as a BorderedContainer with a Text as a content.
	'''

	pass


class TextButton(Button, BorderedContent, content_type=TextString):
	'''\
	Clickable Text with border radius on back.
	Use as a BorderedContainer with a Text as a content.
	'''

	pass


class UpArrowButton(Button, BorderedContent, content_type=UpTriangle):
	'''\
	Used to make up button for numbers setting.
	'''

	pass


class DownArrowButton(Button, BorderedContent, content_type=DownTriangle):
	'''\
	Used to make down button for numbers setting.
	'''

	pass


class ImageButton(Button, BorderedContent, content_type=Image):
	'''\
	Clickable Image with border radius on back.
	Use as a BorderedContainer with an Image as a content.
	'''

	pass


class LineInput(KeyInput, BorderedContent, content_type=TextString):

	def __init__(self, *args, line_len=10, **kwargs):
		super().__init__(*args, **kwargs)
		self.__line_len = line_len

	def callback(self, pos):
		self.is_active = True

	def new_char(self, char: str):
		new_line = self.content.text + char
		if len(new_line) > self.line_len:
			return
		self.content.text = new_line

	def del_char(self):
		self.content.text = self.content.text[:-1]

	def get_line(self) -> str:
		return self.content.text

	@property
	def line_len(self) -> int:
		return self.__line_len

	@line_len.setter
	def line_len(self, line_len: int):
		self.__line_len = line_len
		return self.lien_len

