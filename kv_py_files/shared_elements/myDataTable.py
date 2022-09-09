import functools

from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from typing import Callable


class ClickableBoxLayout(ButtonBehavior, BoxLayout):
    obj = None

    def __init__(self, bg_color, **kwargs):
        # make sure we aren't overriding any important functionality
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(rgba=bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def change_color(self, bg_color):
        with self.canvas.before:
            Color(rgba=bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)


class MyDataTable(BoxLayout):
    is_row_selected: BooleanProperty = BooleanProperty(False)
    object_selected: ObjectProperty = ObjectProperty(None, allownone=True)
    row_selected = None
    gridLayout_rows: GridLayout
    # dp() should probably be used
    height_row: float
    # columns_names will be displayed in first row
    columns_names: tuple[str]
    # attr_names will be used in getattr()
    attr_names: tuple[str]
    # attr_func functions that will be called on each attribute
    attr_func: tuple[Callable[[object], str]]
    # relative widths that should add up to 1
    columns_widths: tuple[float]
    bg_color: tuple[float]
    selected_color: tuple[float]
    not_selected_color: tuple[float]
    list_objects: ListProperty = ListProperty()

    def __init__(self, **kwargs):
        self.bg_color = kwargs.pop('bg_color')
        self.selected_color = kwargs.pop('selected_color')
        self.not_selected_color = kwargs.pop('not_selected_color')
        self.height_row = kwargs.pop('height_row')
        self.columns_names = kwargs.pop('columns_names')
        self.attr_names = kwargs.pop('attr_names')
        self.columns_widths = kwargs.pop('columns_widths')
        if 'attr_func' in kwargs:
            self.attr_func = kwargs.pop('attr_func')
        else:
            self.attr_func = tuple([self.check_none for _ in range(len(self.attr_names))])
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=self.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.orientation = 'vertical'
        main_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=self.height_row)
        for column_name, column_width in zip(self.columns_names, self.columns_widths):
            label = Label(text=column_name, size_hint=(column_width, 1))
            main_row.add_widget(label)
        self.add_widget(main_row)

        scrollView = ScrollView()
        gridLayout = GridLayout()
        gridLayout.cols = 1
        gridLayout.size_hint = (1, None)
        gridLayout.bind(minimum_height=gridLayout.setter('height'))
        scrollView.add_widget(gridLayout)
        self.gridLayout_rows = gridLayout
        self.add_widget(scrollView)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    # called when self.list_objects changes
    def on_list_objects(self, myDataTable, new_list_objects):
        self.is_row_selected = False
        self.object_selected = None
        self.row_selected = None
        self.gridLayout_rows.clear_widgets()

        for obj in new_list_objects:
            row = ClickableBoxLayout(bg_color=self.not_selected_color, orientation='horizontal', size_hint=(1, None), height=self.height_row)
            row.obj = obj
            row.bind(on_press=self.row_select)
            values = []
            for attr_name in self.attr_names:
                values.append(self.rgetattr(obj, attr_name))
            for value, func, width in zip(values, self.attr_func, self.columns_widths):
                label = Label(size_hint=(width, 1))
                label.text = func(value)
                row.add_widget(label)
            self.gridLayout_rows.add_widget(row)

    def row_select(self, row):
        self.is_row_selected = True
        self.object_selected = row.obj

        if self.row_selected is not None:
            self.row_selected.change_color(self.not_selected_color)
        self.row_selected = row
        self.row_selected.change_color(self.selected_color)

    @staticmethod
    def check_none(obj: object) -> str:
        if obj is None:
            return ''
        else:
            return str(obj)

    # getattr that works on nested objects
    # ref: https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-subobjects-chained-properties
    @staticmethod
    def rgetattr(obj, attr, *args):
        def _getattr(obj, attr):
            return getattr(obj, attr, *args)
        return functools.reduce(_getattr, [obj] + attr.split('.'))
