from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen

from entities.owner import Owner
from kv_py_files.dogsApp import app
from controller.errors import InsertOwnerError


class AddClientScreen(Screen):
    has_already_added = BooleanProperty(False)

    def on_pre_enter(self, *args):
        self.ids['txt_input_phone_number'].text = ''
        self.ids['txt_input_first_name'].text = ''
        self.ids['txt_input_last_name'].text = ''
        self.ids['txt_input_note'].text = ''
        self.ids['status_label'].reset_to_default()
        self.has_already_added = False

    def on_add_button_click(self):
        phone_number = self.ids['txt_input_phone_number'].text
        first_name = self.ids['txt_input_first_name'].text
        last_name = self.ids['txt_input_last_name'].text
        note = self.ids['txt_input_note'].text

        new_owner = Owner(id=None, phone=phone_number,first_name=first_name, last_name=last_name, note=note, dogs=None)
        try:
            self.ids['status_label'].text = 'Dodawanie...'
            app.controller.add_owner(new_owner)
            self.has_already_added = True
            self.ids['status_label'].text = 'Dodano użytkowika'
        except InsertOwnerError as err:
            self.ids['status_label'].text = err.msg
        self.ids['status_label'].change_color((191 / 255, 64 / 255, 191 / 255, 1))
