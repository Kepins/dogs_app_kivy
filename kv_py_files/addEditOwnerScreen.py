from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.screenmanager import Screen


from entities.owner import Owner
from kv_py_files.dogsApp import app


class AddEditOwnerScreen(Screen):
    prev_screen: str = None
    title_label_text = StringProperty()
    accept_button_text = StringProperty()
    accept_button_disabled = BooleanProperty(False)
    edit_dogs_button_disabled = BooleanProperty(True)

    # mode in which screen operates
    # if adding==True then screen will allow to add client
    # else screen will allow to edit client
    adding: bool = False
    # owner_edited will be used if adding==False
    owner_edited = None

    def on_pre_enter(self, *args):
        self.set_widgets()

    def accept_button_click(self):
        if self.adding:
            self.add_owner()
        else:
            self.edit_owner()

    def set_widgets(self):
        self.accept_button_disabled = False
        self.ids['status_label'].reset_to_default()
        # adding new owner
        if self.adding:
            # title text
            self.title_label_text = 'Dodawanie klienta'
            # accept button text
            self.accept_button_text = 'Dodaj'
            # edit dogs button
            self.edit_dogs_button_disabled = True
            # inputs
            self.ids['txt_input_phone_number'].text = ''
            self.ids['txt_input_phone_name'].text = ''
            self.ids['txt_input_first_name'].text = ''
            self.ids['txt_input_last_name'].text = ''
            self.ids['txt_input_note'].text = ''

        # editing existing owner
        else:
            # title text
            self.title_label_text = 'Edytowanie klienta'
            # accept button text
            self.accept_button_text = 'Zapisz'
            # edit dogs button
            self.edit_dogs_button_disabled = False
            # inputs
            filter_none = lambda x: '' if(x is None) else x
            self.ids['txt_input_phone_number'].text = filter_none(self.owner_edited.phone_number)
            self.ids['txt_input_phone_name'].text = filter_none(self.owner_edited.phone_name)
            self.ids['txt_input_first_name'].text = filter_none(self.owner_edited.first_name)
            self.ids['txt_input_last_name'].text = filter_none(self.owner_edited.last_name)
            self.ids['txt_input_note'].text = filter_none(self.owner_edited.note)

    def add_owner(self):
        phone_number = self.ids['txt_input_phone_number'].text
        phone_name = self.ids['txt_input_phone_name'].text
        first_name = self.ids['txt_input_first_name'].text
        last_name = self.ids['txt_input_last_name'].text
        note = self.ids['txt_input_note'].text

        new_owner = Owner(id=None, phone_number=phone_number, phone_name=phone_name,
                          first_name=first_name, last_name=last_name, note=note)

        self.ids['status_label'].text = 'Dodawanie...'
        new_owner = app.controller.add_owner(new_owner)
        self.accept_button_disabled = True
        self.ids['status_label'].text = 'Dodano użytkownika'
        # change mode of the screen
        self.owner_edited = new_owner
        self.adding = False
        self.edit_dogs_button_disabled = False
        self.ids['status_label'].change_color((191 / 255, 64 / 255, 191 / 255, 1))

    def edit_owner(self):
        phone_number = self.ids['txt_input_phone_number'].text
        phone_name = self.ids['txt_input_phone_name'].text
        first_name = self.ids['txt_input_first_name'].text
        last_name = self.ids['txt_input_last_name'].text
        note = self.ids['txt_input_note'].text

        edited_owner = Owner(id=self.owner_edited.id, phone_number=phone_number, phone_name=phone_name,
                             first_name=first_name, last_name=last_name, note=note)

        self.ids['status_label'].text = 'Edytowanie...'
        self.owner_edited = app.controller.edit_owner(edited_owner)
        self.ids['status_label'].text = 'Edytowano'

        self.ids['status_label'].change_color((191 / 255, 64 / 255, 191 / 255, 1))
