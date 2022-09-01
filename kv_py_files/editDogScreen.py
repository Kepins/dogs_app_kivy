from kivy.metrics import dp
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen

from entities.dog import Dog
from kv_py_files.dogsApp import app
from kv_py_files.shared_elements.buttonWithBreed import ButtonWithBreed
from kv_py_files.shared_elements.buttonWithSize import ButtonWithSize




class EditDogScreen(Screen):
    dog: Dog
    breeds_dropdown: DropDown
    sizes_dropdown: DropDown
    dropdown_buttons_initialized = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.breeds_dropdown = DropDown()
        self.sizes_dropdown = DropDown()

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
        self.breeds_dropdown.clear_widgets()
        for breed in breeds:
            btn = ButtonWithBreed()
            btn.breed = breed
            btn.text = breed.name
            btn.size_hint = (1, None)
            btn.height = dp(30)
            btn.background_normal = ''
            btn.background_color = (220 / 255, 220 / 255, 220 / 255, 1)
            btn.bind(on_release=lambda btn: self.breeds_dropdown.select(btn.breed))
            self.breeds_dropdown.add_widget(btn)

        # size dropdown
        button_size = self.ids['button_size_dropdown']
        button_size.my_size = dog.size
        button_size.text = dog.size.name
        self.sizes_dropdown.clear_widgets()
        for size in sizes:
            btn = ButtonWithSize()
            btn.my_size = size
            btn.text = size.name
            btn.size_hint = (1, None)
            btn.height = dp(30)
            btn.background_normal = ''
            btn.background_color = (220 / 255, 220 / 255, 220 / 255, 1)
            btn.bind(on_release=lambda btn: self.sizes_dropdown.select(btn.my_size))
            self.sizes_dropdown.add_widget(btn)

        if not self.dropdown_buttons_initialized:
            button_breed.bind(on_release=self.breeds_dropdown.open)
            self.breeds_dropdown.bind(on_select=lambda instance, breed: (
            setattr(button_breed, 'breed', breed), setattr(button_breed, 'text', breed.name)))
            button_size.bind(on_release=self.sizes_dropdown.open)
            self.sizes_dropdown.bind(on_select=lambda instance, my_size: (
            setattr(button_size, 'my_size', my_size), setattr(button_size, 'text', my_size.name)))

    def on_save_button_click(self):
        input_name = self.ids['txt_input_name']
        breed = self.ids['button_breed_dropdown'].breed
        size = self.ids['button_size_dropdown'].my_size
        input_note = self.ids['txt_input_note']
        name = input_name.text
        note = input_note.text
        print(name, breed, size, note)
