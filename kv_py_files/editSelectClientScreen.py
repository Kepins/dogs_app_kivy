from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.screenmanager import Screen


from kv_py_files.dogsApp import app


class EditSelectClientScreen(Screen):
    phone_number: str
    phone_name: str
    last_name: str
    is_row_selected = BooleanProperty(False)
    owner_selected = ObjectProperty(None, allownone=True)
    bound = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        # reset to default state
        self.phone_number = ''
        self.phone_name = ''
        self.last_name = ''
        self.ids['txt_input_phone_number'].text = ''
        self.ids['txt_input_phone_name'].text = ''
        self.ids['txt_input_last_name'].text = ''

        if not self.bound:
            dogsDataTable = self.ids['clientsDataTable']
            dogsDataTable.bind(is_row_selected=self.setter('is_row_selected'))
            dogsDataTable.bind(object_selected=self.setter('owner_selected'))
            self.bound = True

        self.update_rows()

    def update_rows(self):
        dogsDataTable = self.ids['clientsDataTable']
        dogsDataTable.list_objects = []
        dogsDataTable.list_objects = app.controller.get_owners(phone_number=str(self.phone_number),
                                                               phone_name=str(self.phone_name),
                                                               last_name=str(self.last_name))
