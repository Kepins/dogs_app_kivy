import functools
from typing import Callable

from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown


class ButtonWithObject(Button):
    obj = None

    def __init__(self, obj=None, **kwargs):
        super().__init__(**kwargs)
        self.obj = obj


class MyDropDown(DropDown):
    main_button: ButtonWithObject
    height_row: float
    btn_color: tuple[float]
    # if attr_name is None then obj ButtonWithObject.obj is used
    # else ButtonWithObject.obj.attr_name is used
    attr_name = None
    attr_func: Callable[[object], str]
    list_objects: ListProperty = ListProperty()

    def __init__(self, **kwargs):
        self.height_row = kwargs.pop('height_row')
        self.btn_color = kwargs.pop('btn_color')
        self.attr_name = kwargs.pop('attr_name')
        if 'attr_func' in kwargs:
            self.attr_func = kwargs.pop('attr_func')
        else:
            self.attr_func = self.check_none
        super().__init__(**kwargs)

    def bind_button(self, main_button: ButtonWithObject):
        self.main_button = main_button
        self.main_button.color = (0, 0, 0, 1)
        self.main_button.bind(on_release=self.open)
        self.bind(on_select=lambda instance, obj: self.update_main_button(obj))

    def update_main_button(self, obj: object):
        self.main_button.obj = obj
        if self.attr_name is not None:
            val = self.rgetattr(obj, self.attr_name)
        else:
            val = obj
        self.main_button.text = self.attr_func(val)

    def on_list_objects(self, myDropDown, new_list_objects):
        self.clear_widgets()
        for obj in new_list_objects:
            button_with_obj = ButtonWithObject(obj)
            if self.attr_name is not None:
                val = self.rgetattr(obj, self.attr_name)
            else:
                val = obj
            button_with_obj.text = self.attr_func(val)
            button_with_obj.color = (0, 0, 0, 1)
            button_with_obj.size_hint = (1, None)
            button_with_obj.height = self.height_row
            button_with_obj.background_normal = ''
            button_with_obj.background_color = self.btn_color
            button_with_obj.bind(on_release=lambda btn: self.select(btn.obj))
            self.add_widget(button_with_obj)

    @staticmethod
    def check_none(obj: object) -> str:
        if obj is None:
            return ''
        else:
            return str(obj)

    @staticmethod
    def rgetattr(obj, attr, *args):
        def _getattr(obj, attr):
            return getattr(obj, attr, *args)
        return functools.reduce(_getattr, [obj] + attr.split('.'))

