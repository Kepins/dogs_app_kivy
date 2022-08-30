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
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from controller import Controller
# entities
from entities.breed import Breed
from entities.dog import Dog
from entities.owner import Owner


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
        note = self.ids.txt_input_note.text

        print('phone: {}\nfirst name: {}\nlast name: {}\nnote: {}'.format(phone_number, first_name, last_name, note))


class EditSelectClientScreen(Screen):
    phone_number: str
    first_name: str
    last_name: str
    is_row_selected = BooleanProperty(False)
    owner_selected: Owner

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        # reset to default statre
        self.phone_number = ''
        self.first_name = ''
        self.last_name = ''
        self.ids['txt_input_phone_number'].text = ''
        self.ids['txt_input_first_name'].text = ''
        self.ids['txt_input_last_name'].text = ''
        self.ids['clientsDataTable'].update_data_rows()

    def update_data(self):
        self.ids['clientsDataTable'].update_data_rows(str(self.phone_number), str(self.first_name), str(self.last_name))


class EditClientScreen(Screen):
    owner_edited: Owner

    def on_pre_enter(self, *args):
        owner = app.root.get_screen('editSelectClientScreen').owner_selected
        self.owner_edited = owner
        input_phone_number = self.ids['txt_input_phone_number']
        input_first_name = self.ids['txt_input_first_name']
        input_last_name = self.ids['txt_input_last_name']
        input_note = self.ids['txt_input_note']

        input_phone_number.text = owner.phone
        input_phone_number.disabled = True
        if owner.first_name is not None:
            input_first_name.text = owner.first_name
        else:
            input_first_name.text = ''
        if owner.last_name is not None:
            input_last_name.text = owner.last_name
        else:
            input_last_name.text = ''
        if owner.note is not None:
            input_note.text = owner.note
        else:
            input_note.text = ''

    def on_save_button_click(self):
        input_first_name = self.ids['txt_input_first_name']
        input_last_name = self.ids['txt_input_last_name']
        input_note = self.ids['txt_input_note']
        first_name = input_first_name.text
        last_name = input_last_name.text
        note = input_note.text
        print(first_name, last_name, note)


class EditSelectDogScreen(Screen):
    owner_edited: Owner
    is_row_selected = BooleanProperty(False)
    dog_selected: Owner

    def on_pre_enter(self, *args):
        owner = app.root.get_screen('editClientScreen').owner_edited
        self.owner_edited = owner
        self.ids['dogsDataTable'].update_data_rows()


class EditDogScreen(Screen):
    dog: Dog

    def on_pre_enter(self, *args):
        dog = app.root.get_screen('editSelectDogScreen').dog_selected
        self.dog = dog
        input_name = self.ids['txt_input_name']
        input_note = self.ids['txt_input_note']
        if dog.name is not None:
            input_name.text = self.dog.name
        else:
            input_name.text = ''
        if dog.note is not None:
            input_note.text = dog.note
        else:
            input_note.text = ''

        breeds = app.controller.get_breeds()

        sizes = app.controller.get_sizes()

        # breed dropdown
        button_breed = self.ids['button_breed_dropdown']
        button_breed.breed = dog.breed
        button_breed.text = dog.breed.name
        breeds_dropdown = DropDown()
        for breed in breeds:
            btn = ButtonWithBreed()
            btn.breed = breed
            btn.text = breed.name
            btn.size_hint = (1, None)
            btn.height = dp(30)
            btn.background_normal = ''
            btn.background_color = (220/255, 220/255, 220/255, 1)
            btn.bind(on_release=lambda btn: breeds_dropdown.select(btn.breed))
            breeds_dropdown.add_widget(btn)

        button_breed.bind(on_release=breeds_dropdown.open)
        breeds_dropdown.bind(on_select=lambda instance, breed: (setattr(button_breed, 'breed', breed), setattr(button_breed, 'text', breed.name)))

        # size dropdown
        button_size = self.ids['button_size_dropdown']
        button_size.my_size = dog.size
        button_size.text = dog.size.name
        sizes_dropdown = DropDown()
        for size in sizes:
            btn = ButtonWithSize()
            btn.my_size = size
            btn.text = size.name
            btn.size_hint = (1, None)
            btn.height = dp(30)
            btn.background_normal = ''
            btn.background_color = (220 / 255, 220 / 255, 220 / 255, 1)
            btn.bind(on_release=lambda btn: sizes_dropdown.select(btn.my_size))
            sizes_dropdown.add_widget(btn)

        button_size.bind(on_release=sizes_dropdown.open)
        sizes_dropdown.bind(on_select=lambda instance, my_size: (setattr(button_size, 'my_size', my_size), setattr(button_size, 'text', my_size.name)))

    def on_save_button_click(self):
        input_name = self.ids['txt_input_name']
        input_note = self.ids['txt_input_note']
        name = input_name.text
        note = input_note.text
        print(name, note)

class WindowManager(ScreenManager):
    pass


# should be used in dropdown
class ButtonWithBreed(Button):
    breed = None


# should be used in dropdown
class ButtonWithSize(Button):
    my_size = None


# should be used in ClientsDataTable, DogsDataTable
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
        owners = DogsApp.controller.get_owners(phone=phone, first_name=first_name, last_name=last_name)
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


class DogsDataTable(BoxLayout):
    row_selected = None
    gridLayout_rows: GridLayout

    height_row = dp(30)
    columns = ['imię', 'rasa', 'wielkość', 'notka']
    column_widths = (4/18, 5/18, 3/18, 6/18)
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

    def update_data_rows(self):
        # update root
        self.root.is_row_selected = False
        self.root.dog_selected = None

        self.row_selected = None
        gridLayout = self.gridLayout_rows
        gridLayout.clear_widgets()

        owner = self.root.owner_edited
        dogs = owner.dogs

        for dog in dogs:
            row = ClickableBoxLayout(bg_color=self.bg_color, orientation='horizontal', size_hint=(1, None),
                                     height=self.height_row)
            row.dog = dog
            row.bind(on_press=self.on_row_select)
            values = (dog.name, dog.breed.name, dog.size.name, dog.note)
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
        self.root.dog_selected = row.dog

        if self.row_selected:
            self.row_selected.change_color(self.bg_color)
        self.row_selected = row
        self.row_selected.change_color(self.selected_color)

class DogsApp(App):
    controller = Controller()


if __name__ == '__main__':
    app = DogsApp()
    app.run()
