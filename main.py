from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from controller import Controller


# Define different screens
class WelcomeScreen(Screen):
    pass


class ClientsScreen(Screen):
    pass


class AddClientScreen(Screen):
    def on_add_button_click(self):
        phone_number = self.ids.txt_input_phone_number.text
        first_name = self.ids.txt_input_first_name.text
        last_name = self.ids.txt_input_last_name.text

        print('phone: {}\nfirst name: {}\nlast name: {}'.format(phone_number, first_name, last_name))


class EditSelectClientScreen(Screen):
    phone_number: str
    first_name: str
    last_name: str
    is_row_selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.phone_number = ''
        self.first_name = ''
        self.last_name = ''

    def update_data(self):
        self.ids['clientsDataTable'].update_data_rows(str(self.phone_number), str(self.first_name), str(self.last_name))


class WindowManager(ScreenManager):
    pass


# should be used in ClientsDataTable
class ClickableBoxLayout(ButtonBehavior, BoxLayout):
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


class ClientsDataTable(BoxLayout):
    row_selected = None
    data_rows: [ClickableBoxLayout]
    gridLayout_rows: GridLayout

    height_row = dp(30)
    columns = ['telefon', 'imię', 'nazwisko']
    column_widths = (1/3, 1/3, 1/3)
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
        self.update_data_rows()
        self.add_widget(scrollView)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_data_rows(self, phone='', first_name='', last_name=''):
        if hasattr(self, 'root'):
            self.root.is_row_selected = False
        self.row_selected = None
        self.data_rows = []
        gridLayout = self.gridLayout_rows
        gridLayout.clear_widgets()
        owners = DogsApp.controller.get_owners(phone=phone, first_name=first_name, last_name=last_name)
        for owner in owners:
            row = ClickableBoxLayout(bg_color=self.bg_color, orientation='horizontal', size_hint=(1, None),
                                     height=self.height_row)
            row.bind(on_press=self.on_row_select)
            values = (owner.phone, owner.first_name, owner.last_name)
            for value, width in zip(values, self.column_widths):
                label = Label(size_hint=(width, 1))
                if value is not None:
                    label.text = value
                else:
                    label.text = ''
                row.add_widget(label)
            self.data_rows.append(row)
            gridLayout.add_widget(row)

    def on_row_select(self, row):
        if hasattr(self, 'root'):
            self.root.is_row_selected = True
        if self.row_selected:
            self.row_selected.change_color(self.bg_color)
        self.row_selected = row
        self.row_selected.change_color(self.selected_color)


class DogsApp(App):
    controller = Controller()


if __name__ == '__main__':
    DogsApp().run()
