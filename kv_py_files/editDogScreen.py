from kivy.metrics import dp
from kivy.uix.screenmanager import Screen

from controller.errors import EditDogError
from entities.dog import Dog
from kv_py_files.dogsApp import app
from kv_py_files.shared_elements.myDropDown import MyDropDown


class EditDogScreen(Screen):
    dog: Dog
    breeds_dropdown: MyDropDown
    sizes_dropdown: MyDropDown
    dropdown_buttons_initialized = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.breeds_dropdown = MyDropDown(height_row=dp(30), btn_color=(220/255, 220/255, 220/255, 1), attr_name='name')
        self.sizes_dropdown = MyDropDown(height_row=dp(30), btn_color=(220/255, 220/255, 220/255, 1), attr_name='name')

    def on_pre_enter(self, *args):
        dog = self.dog
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

        # init button dropdowns once in app run
        if not self.dropdown_buttons_initialized:
            button_breed = self.ids['button_breed_dropdown']
            button_size = self.ids['button_size_dropdown']
            self.breeds_dropdown.bind_button(main_button=button_breed)
            self.sizes_dropdown.bind_button(main_button=button_size)

        # change on every screen load
        self.breeds_dropdown.list_objects = breeds
        self.sizes_dropdown.list_objects = sizes
        self.breeds_dropdown.update_main_button(obj=self.dog.breed)
        self.sizes_dropdown.update_main_button(obj=self.dog.size)

        # reset to default
        self.ids['status_label'].reset_to_default()

    def on_save_button_click(self):
        input_name = self.ids['txt_input_name']
        breed = self.ids['button_breed_dropdown'].obj
        size = self.ids['button_size_dropdown'].obj
        input_note = self.ids['txt_input_note']
        name = input_name.text
        note = input_note.text
        edited_dog = Dog(id=self.dog.id, owner=self.dog.owner, name=name, breed=breed, size=size, note=note, appointments=self.dog.appointments)
        try:
            self.ids['status_label'].text = 'Edytowanie...'
            app.controller.edit_dog(edited_dog)
            self.ids['status_label'].text = 'Edytowano'
        except EditDogError as err:
            self.ids['status_label'].text = err.msg
        self.ids['status_label'].change_color((191 / 255, 64 / 255, 191 / 255, 1))

