from mysql.connector.errors import Error
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen

from entities.owner import Owner
from kv_py_files.dogsApp import app


class AddClientScreen(Screen):
    has_already_added = BooleanProperty(False)

    def on_pre_enter(self, *args):
        self.ids['txt_input_phone_number'].text = ''
        self.ids['txt_input_first_name'].text = ''
        self.ids['txt_input_last_name'].text = ''
        self.ids['txt_input_note'].text = ''
        self.ids['status_label'].reset_to_default()

    def on_add_button_click(self):
        phone_number = self.ids['txt_input_phone_number'].text
        first_name = self.ids['txt_input_first_name'].text
        last_name = self.ids['txt_input_last_name'].text
        note = self.ids['txt_input_note'].text

        new_owner = Owner(id=None, phone=phone_number,first_name=first_name, last_name=last_name, note=note, dogs=None)
        try:
            app.controller.add_owner(new_owner)
            self.ids['status_label'].text = 'Dodano'
            self.has_already_added = True
        except Error as err:
            print(err)
            self.ids['status_label'].text = 'Błąd'

        self.ids['status_label'].change_color((191 / 255, 64 / 255, 191 / 255, 1))
        print('phone: {}\nfirst name: {}\nlast name: {}\nnote: {}'.format(phone_number, first_name, last_name, note))