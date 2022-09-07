from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen

from controller.errors import InsertDogError
from entities.breed import Breed
from entities.dog import Dog
from entities.owner import Owner
from entities.size import Size
from kv_py_files.dogsApp import app
from kv_py_files.shared_elements.myDropDown import MyDropDown


class AddDogScreen(Screen):
    owner: Owner
    breeds_dropdown: MyDropDown
    sizes_dropdown: MyDropDown
    dropdown_buttons_initialized = False
    has_already_added = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.breeds_dropdown = MyDropDown(height_row=dp(30), btn_color=(220/255, 220/255, 220/255, 1), attr_name='name')
        self.sizes_dropdown = MyDropDown(height_row=dp(30), btn_color=(220/255, 220/255, 220/255, 1), attr_name='name')

    def on_pre_enter(self, *args):
        owner = app.root.get_screen('editSelectDogScreen').owner_edited
        self.owner = owner
        input_name = self.ids['txt_input_name']
        input_note = self.ids['txt_input_note']

        input_name.text = ''
        input_note.text = ''

        breeds = app.controller.get_breeds()

        sizes = app.controller.get_sizes()

        Breed(id=None, name='Wybierz rasę', dogs=[])
        Size(id=None, name='Wybierz wielkość', dogs=[])

        # init button dropdowns once in app run
        if not self.dropdown_buttons_initialized:
            button_breed = self.ids['button_breed_dropdown']
            button_size = self.ids['button_size_dropdown']
            self.breeds_dropdown.bind_button(main_button=button_breed)
            self.sizes_dropdown.bind_button(main_button=button_size)

        # change on every screen load
        self.breeds_dropdown.list_objects = breeds
        self.sizes_dropdown.list_objects = sizes
        self.breeds_dropdown.update_main_button(obj=Breed(id=None, name='Wybierz rasę', dogs=[]))
        self.sizes_dropdown.update_main_button(obj=Size(id=None, name='Wybierz wielkość', dogs=[]))
        # reset to default
        self.ids['status_label'].reset_to_default()
        self.has_already_added = False

    def on_add_button_click(self):
        input_name = self.ids['txt_input_name']
        breed = self.ids['button_breed_dropdown'].obj
        size = self.ids['button_size_dropdown'].obj
        input_note = self.ids['txt_input_note']
        name = input_name.text
        note = input_note.text
        owner = self.owner

        new_dog = Dog(id=None, owner=owner, name=name, breed=breed, size=size, note=note, appointments=None)
        try:
            self.ids['status_label'].text = 'Dodawanie...'
            app.controller.add_dog(new_dog)
            self.has_already_added = True
            self.ids['status_label'].text = 'Dodano psa'
        except InsertDogError as err:
            self.ids['status_label'].text = err.msg
        self.ids['status_label'].change_color((191 / 255, 64 / 255, 191 / 255, 1))



