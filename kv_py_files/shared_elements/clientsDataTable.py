from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from kv_py_files.dogsApp import app
from kv_py_files.shared_elements.clickableBoxLayout import ClickableBoxLayout


class ClientsDataTable(BoxLayout):
    row_selected = None
    gridLayout_rows: GridLayout

    height_row = dp(30)
    columns = ['telefon', 'imię', 'nazwisko', 'notka']
    column_widths = (4/18, 4/18, 4/18, 6/18)
    bg_color = ListProperty([220/255, 220/255, 220/255, 1])
    selected_color = ListProperty([0, 220/255, 220/255, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=self.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)
        self.orientation = 'vertical'
        main_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=self.height_row)
        for column, width in zip(self.columns, self.column_widths):
            label = Label(text=column, size_hint=(width, 1))
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

    def update_data_rows(self, phone='', first_name='', last_name=''):
        # update root
        self.root.is_row_selected = False
        self.root.owner_selected = None

        self.row_selected = None
        gridLayout = self.gridLayout_rows
        gridLayout.clear_widgets()
        owners = app.controller.get_owners(phone=phone, first_name=first_name, last_name=last_name)
        for owner in owners:
            row = ClickableBoxLayout(bg_color=self.bg_color, orientation='horizontal', size_hint=(1, None),
                                     height=self.height_row)
            row.owner = owner
            row.bind(on_press=self.on_row_select)
            values = (owner.phone, owner.first_name, owner.last_name, owner.note)
            for value, width in zip(values, self.column_widths):
                label = Label(size_hint=(width, 1))
                if value is not None:
                    label.text = value
                else:
                    label.text = ''
                row.add_widget(label)
            gridLayout.add_widget(row)

    def on_row_select(self, row):
        # update root
        self.root.is_row_selected = True
        self.root.owner_selected = row.owner

        if self.row_selected:
            self.row_selected.change_color(self.bg_color)
        self.row_selected = row
        self.row_selected.change_color(self.selected_color)
