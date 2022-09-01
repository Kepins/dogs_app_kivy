from kivy.uix.screenmanager import Screen

from entities.owner import Owner
from kv_py_files.dogsApp import app


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
