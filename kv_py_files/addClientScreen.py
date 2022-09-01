from kivy.uix.screenmanager import Screen


class AddClientScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids['txt_input_phone_number'].text = ''
        self.ids['txt_input_first_name'].text = ''
        self.ids['txt_input_last_name'].text = ''
        self.ids['txt_input_note'].text = ''
    def on_add_button_click(self):
        phone_number = self.ids['txt_input_phone_number'].text
        first_name = self.ids['txt_input_first_name'].text
        last_name = self.ids['txt_input_last_name'].text
        note = self.ids['txt_input_note'].text

        print('phone: {}\nfirst name: {}\nlast name: {}\nnote: {}'.format(phone_number, first_name, last_name, note))