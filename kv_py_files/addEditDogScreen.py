from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.screenmanager import Screen

from controller.errors import InsertDogError, EditDogError
from entities.breed import Breed
from entities.dog import Dog
from entities.size import Size
from kv_py_files.dogsApp import app
from kv_py_files.shared_elements.myDropDown import MyDropDown


class AddEditDogScreen(Screen):
    prev_screen: str = None
    title_label_text = StringProperty()
    accept_button_text = StringProperty()
    accept_button_disabled = BooleanProperty(False)

    # mode in which screen operates
    # if adding==True then screen will allow to add dog
    # else screen will allow to edit dog
    adding: bool = False
    owner = None
    # dog_edited will be used if adding==False
    dog_edited = None

    dropdown_buttons_initialized = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.breeds_dropdown = MyDropDown(height_row=dp(30), btn_color=(220/255, 220/255, 220/255, 1), attr_name='name')
        self.sizes_dropdown = MyDropDown(height_row=dp(30), btn_color=(220/255, 220/255, 220/255, 1), attr_name='name')

    def on_pre_enter(self, *args):
        # init button dropdowns once in app run
        if not self.dropdown_buttons_initialized:
            button_breed = self.ids['button_breed_dropdown']
            button_size = self.ids['button_size_dropdown']
            self.breeds_dropdown.bind_button(main_button=button_breed)
            self.sizes_dropdown.bind_button(main_button=button_size)
        self.set_widgets()

    def accept_button_click(self):
        if self.adding:
            self.add_dog()
        else:
            self.edit_dog()

    def set_widgets(self):
        self.accept_button_disabled = False
        self.ids['status_label'].reset_to_default()

        # dropdowns load
        breeds = app.controller.get_breeds()
        sizes = app.controller.get_sizes()
        self.breeds_dropdown.list_objects = breeds
        self.sizes_dropdown.list_objects = sizes
        # adding new dog
        if self.adding:
            # title text
            self.title_label_text = 'Dodawanie psa'
            # accept button text
            self.accept_button_text = 'Dodaj'
            # inputs
            self.ids['txt_input_name'].text = ''
            self.ids['txt_input_note'].text = ''
            # dropdowns default value
            self.breeds_dropdown.update_main_button(obj=Breed(id=None, name='Wybierz rasę', dogs=[]))
            self.sizes_dropdown.update_main_button(obj=Size(id=None, name='Wybierz wielkość', dogs=[]))

        # editing existing dog
        else:
            # title text
            self.title_label_text = 'Edytowanie psa'
            # accept button text
            self.accept_button_text = 'Zapisz'
            # inputs
            filter_none = lambda x: '' if (x is None) else x
            self.ids['txt_input_name'].text = filter_none(self.dog_edited.name)
            self.ids['txt_input_note'].text = filter_none(self.dog_edited.note)
            # dropdowns default value
            self.breeds_dropdown.update_main_button(obj=self.dog_edited.breed)
            self.sizes_dropdown.update_main_button(obj=self.dog_edited.size)

    def add_dog(self):
        name = self.ids['txt_input_name'].text
        breed = self.ids['button_breed_dropdown'].obj
        size = self.ids['button_size_dropdown'].obj
        note = self.ids['txt_input_note'].text
        owner = self.owner

        new_dog = Dog(id=None, owner=owner, name=name, breed=breed, size=size, note=note, appointments=[])
        try:
            self.ids['status_label'].text = 'Dodawanie...'
            app.controller.add_dog(new_dog)
            self.accept_button_disabled = True
            self.ids['status_label'].text = 'Dodano psa'
            self.dog_edited = new_dog
            self.adding = False
        except InsertDogError as err:
            self.ids['status_label'].text = err.msg
        self.ids['status_label'].change_color((191 / 255, 64 / 255, 191 / 255, 1))

    def edit_dog(self):
        name = self.ids['txt_input_name'].text
        breed = self.ids['button_breed_dropdown'].obj
        size = self.ids['button_size_dropdown'].obj
        note = self.ids['txt_input_note'].text
        owner = self.owner

        edited_dog = Dog(id=self.dog_edited.id, owner=self.dog_edited.owner, name=name, breed=breed, size=size, note=note,
                         appointments=self.dog_edited.appointments)
        try:
            self.ids['status_label'].text = 'Edytowanie...'
            app.controller.edit_dog(edited_dog)
            self.ids['status_label'].text = 'Edytowano'
        except EditDogError as err:
            self.ids['status_label'].text = err.msg
        self.ids['status_label'].change_color((191 / 255, 64 / 255, 191 / 255, 1))

