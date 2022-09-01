from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen

from entities.dog import Dog
from entities.owner import Owner
from kv_py_files.dogsApp import app


class EditSelectDogScreen(Screen):
    owner_edited: Owner
    is_row_selected = BooleanProperty(False)
    dog_selected: Dog

    def on_pre_enter(self, *args):
        owner = app.root.get_screen('editClientScreen').owner_edited
        self.owner_edited = owner
        self.ids['dogsDataTable'].update_data_rows()
