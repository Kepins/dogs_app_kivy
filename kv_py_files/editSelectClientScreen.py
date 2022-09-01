from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen

from entities.owner import Owner


class EditSelectClientScreen(Screen):
    phone_number: str
    first_name: str
    last_name: str
    is_row_selected = BooleanProperty(False)
    owner_selected: Owner

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        # reset to default state
        self.phone_number = ''
        self.first_name = ''
        self.last_name = ''
        self.ids['txt_input_phone_number'].text = ''
        self.ids['txt_input_first_name'].text = ''
        self.ids['txt_input_last_name'].text = ''
        self.ids['clientsDataTable'].update_data_rows()

    def update_data(self):
        self.ids['clientsDataTable'].update_data_rows(str(self.phone_number), str(self.first_name), str(self.last_name))
