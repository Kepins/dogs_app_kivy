import functools

from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from kv_py_files.shared_elements.clickableBoxLayout import ClickableBoxLayout


class MyDataTable(BoxLayout):
    is_row_selected: BooleanProperty = BooleanProperty(False)
    object_selected: ObjectProperty = ObjectProperty(None)
    row_selected: ClickableBoxLayout | None = None
    gridLayout_rows: GridLayout
    # dp() should probably be used
    height_row: float
    # columns_names will be displayed in first row
    columns_names: tuple[str]
    # attr_names will be used in getattr()
    attr_names: tuple[str]
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
    def on_list_objects(self, dogsDataTable, new_list_objects):
        self.is_row_selected = False
        self.row_selected = None
        self.gridLayout_rows.clear_widgets()

        for obj in new_list_objects:
            row = ClickableBoxLayout(bg_color=self.not_selected_color, orientation='horizontal', size_hint=(1, None), height=self.height_row)
            row.obj = obj
            row.bind(on_press=self.row_select)
            values = []
            for attr_name in self.attr_names:
                values.append(self.rgetattr(obj, attr_name))
            for value, width in zip(values, self.columns_widths):
                label = Label(size_hint=(width, 1))
                if value is not None:
                    label.text = value
                else:
                    label.text = ''
                row.add_widget(label)
            self.gridLayout_rows.add_widget(row)

    def row_select(self, row):
        self.is_row_selected = True
        self.object_selected = row.obj

        if self.row_selected is not None:
            self.row_selected.change_color(self.not_selected_color)
        self.row_selected = row
        self.row_selected.change_color(self.selected_color)

    # getattr that works on nested objects
    # ref: https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-subobjects-chained-properties
    @staticmethod
    def rgetattr(obj, attr, *args):
        def _getattr(obj, attr):
            return getattr(obj, attr, *args)
        return functools.reduce(_getattr, [obj] + attr.split('.'))
