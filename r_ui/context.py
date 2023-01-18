from typing import Set, Dict, List

import pygame

from r_ui.base import UIElement


class Context(UIElement):
	'''\
	Group of ui elements that can show or hide them.
	'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__layers: List[Set[UIElement]] = [set(),]
		self.__ishidden: Dict[UIElement, bool] = {}
		self.__ismuted: Dict[UIElemet, bool] = {}

	def render_onto(self, surf: pygame.Surface):
		for layer in self.__layers:
			for ui_element in layer:
				if self.__ishidden[ui_element]:
					continue
				ui_element.render_onto(surf)

	def event(self, event: pygame.event.EventType):
		for layer in reversed(self.__layers):
			for ui_element in layer:
				if self.__ismuted[ui_element]:
					continue
				ui_element.event(event)

	def add_elem(self, ui_element: UIElement, *args, layer=0):
		'''\
		I advise you this syntax to make layers easy if you add first new layer:
											v
		my_context.add_elem(top_elem, layer=+1)
		'''

		if  not (0 <= layer <= len(self.__layers)):
			return
		if layer == len(self.__layers):
			self.__layers.append(set())
		self.__layers[layer].add(ui_element)
		self.__ishidden[ui_element] = False
		self.__ismuted[ui_element] = False
	
	def rem_elem(self, ui_element: UIElement):
		for layer in self.__layers:
			layer.discard(ui_element)
		self.__ishidden.pop(ui_element)
	
	def show(self, ui_element: UIElement):
		self.__ishidden[ui_element] = False

	def hide(self, ui_element: UIElement):
		self.__ishidden[ui_element] = True

	def loud(self, ui_element: UIElement):
		self.__ismuted[ui_element] = False

	def mute(self, ui_element: UIElement):
		self.__ismuted[ui_element] = True

	def __contain__(self, ui_element: UIElement):
		return any(ui_element in layer for layer in self.__layers)


class ContextSwitcher(Context):
	'''\
	Group of contexts, provide single context displaying and switching
	of actual context. Use to make menus and pages switching.
	'''

	def __init__(self, *args, **kwargs):
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

	def switch(self, title: str):
		self.__actual_context = title

	def get_context(self, title: str):
		return self.__subcontextes.get(title)

	def set_context(self, title: str, context: Context):
		self.__subcontextes[title] = context

	def del_context(self, title: str):
		self.__subcontextes.pop(title)

