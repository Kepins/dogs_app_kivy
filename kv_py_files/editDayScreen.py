from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen

import datetime

import controller.translations as translations
from kv_py_files.dogsApp import app


class EditDayScreen(Screen):
    day: datetime.date
    title = StringProperty()
    is_row_selected = BooleanProperty(False)
    appoint_selected = ObjectProperty(None, allownone=True)
    bound = False

    def on_pre_enter(self, *args):
        self.title = '{} {} {}'.format(str(self.day.day), translations.genitive_months_names[self.day.month], str(self.day.year))
        appointDataTable = self.ids['appointDataTable']
        appointDataTable.list_objects = []
        appointDataTable.list_objects = app.controller.get_appointments(self.day)

        if not self.bound:
            appointDataTable = self.ids['appointDataTable']
            appointDataTable.bind(is_row_selected=self.setter('is_row_selected'))
            appointDataTable.bind(object_selected=self.setter('appoint_selected'))
            self.bound = True
