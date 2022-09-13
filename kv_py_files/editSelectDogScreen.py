from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.screenmanager import Screen

from entities.dog import Dog
from entities.owner import Owner
from kv_py_files.dogsApp import app


class EditSelectDogScreen(Screen):
    prev_screen: str
    owner_edited: Owner
    is_row_selected = BooleanProperty(False)
    dog_selected = ObjectProperty(None, allownone=True)
    bound = False

    def on_pre_enter(self, *args):
        dogsDataTable = self.ids['dogsDataTable']
        dogsDataTable.list_objects = []
        dogsDataTable.list_objects = self.owner_edited.dogs
        if not self.bound:
            dogsDataTable.bind(is_row_selected=self.setter('is_row_selected'))
            dogsDataTable.bind(object_selected=self.setter('dog_selected'))
            self.bound = True
