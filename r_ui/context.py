from typing import Set, Dict

import pygame

from r_ui.base import UIElement


class Context(UIElement):

	def __init__(*args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__elements: Set[UIElement] = set()
		self.__ishidden: Dict[UIElement, bool] = {}

	def render_onto(self, surf: pygame.Surface):
		for ui_element in self.__elements:
			if self.__ishidden[ui_element]:
				continue
			ui_element.render_onto(surf)

	def event(self, event: pygame.event.EventType):
		for ui_element in self.__elements:
			if self.__ishidden[ui_element]:
				continue
			ui_element.event(event)

	def add_elem(self, ui_element: UIElement):
		self.__elements.add(ui_element)
		self.__ishidden[ui_element] = False
	
	def rem_elem(self, ui_element: UIElement):
		self.__elements.discard(ui_element)
		self.__ishidden.pop(ui_element)
	
	def show(self, ui_element: UIElement):
		self.__ishidden[ui_element] = False

	def hide(self, ui_element: UIElement):
		self.__ishidden[ui_element] = True

	def __contain__(self, ui_element: UIElement):
		return ui_element is self.__elements


class ContextSwitcher(Context):

	def __init__(*args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__subcontextes: Dict[str, Context] = {}
		self.__actual_context: str = None

	def render_onto(self, surf: pygame.Surface):
		super().render_onto(surf)
		context = self.__subcontextes.get(self.__actual_context)
		if context is None:
			return
		context.render_onto(surf)

	def event(self, event: pygame.event.EventType):
		super().event(event)
		context = self.__subcontextes.get(self.__actual_context)
		if context is None:
			return
		context.event(event)

	def swicth(self, title: str):
		self.__actual_context = title

	def get_context(self, title: str):
		return self.__subcontextes.get(context)

	def set_context(self, title: str, context: Context):
		self.__subcontextes[title] = context

	def del_context(self, title: str):
		self.__subcontextes.pop(context)

