import datetime
from decimal import Decimal

from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen

from controller import translations
from entities.appointment import Appointment
from entities.owner import Owner
from entities.service import Service
from kv_py_files.dogsApp import app
from kv_py_files.shared_elements.myDropDown import MyDropDown


class AddEditAppointScreen(Screen):
    prev_screen: str = None
    title_label_text = StringProperty()
    day_button_text = StringProperty()
    owner_button_text = StringProperty()
    accept_button_text = StringProperty()

    # mode in which screen operates
    # if adding==True then screen will allow to add appointment
    # else screen will allow to edit appointment
    adding: bool = False
    day = ObjectProperty(None)
    # appoint_edited will be used if adding==False
    appoint_edited = None

    # time selection
    hour_dropdown: MyDropDown
    hours_displayed = [str(i) for i in range(7, 19)]
    min_dropdown: MyDropDown
    mins_displayed = [str(i) for i in range(0, 56, 5)]

    # service selection
    service_dropdown: MyDropDown

    # time selection
    duration_dropdown: MyDropDown
    durations_displayed = [datetime.timedelta(minutes=m)
                           for m in (15, 30, 35, 40, 45, 50, 55, 60, 75, 90, 105, 120)]

    # selectOwner
    owner = ObjectProperty(None, allownone=True)

    # dogsDataTable
    is_dog_selected = BooleanProperty(False)
    dog_selected = ObjectProperty(None, allownone=True)

    # reset widgets
    reset = True

    # after initialization this will be True
    everything_bound: bool = False
    accept_button_disabled = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # time dropdowns
        self.hour_dropdown = MyDropDown(height_row=dp(28), btn_color=(210 / 255, 210 / 255, 210 / 255, 1),
                                        attr_name=None)
        self.min_dropdown = MyDropDown(height_row=dp(28), btn_color=(210 / 255, 210 / 255, 210 / 255, 1),
                                       attr_name=None)

        self.hour_dropdown.list_objects = self.hours_displayed
        self.min_dropdown.list_objects = self.mins_displayed

        # time dropdown
        self.duration_dropdown = MyDropDown(height_row=dp(28), btn_color=(210 / 255, 210 / 255, 210 / 255, 1),
                                            attr_name=None, attr_func=self.timedelta_to_str)
        self.duration_dropdown.list_objects = self.durations_displayed

        # service dropdown
        self.service_dropdown = MyDropDown(height_row=dp(40), btn_color=(210 / 255, 210 / 255, 210 / 255, 1),
                                           attr_name='name')

    def on_pre_enter(self, *args):
        # once in app run
        if not self.everything_bound:
            # time dropdowns
            button_hour = self.ids['button_hour_dropdown']
            button_min = self.ids['button_min_dropdown']
            self.hour_dropdown.bind_button(main_button=button_hour)
            self.min_dropdown.bind_button(main_button=button_min)

            # duration dropdown
            button_duration = self.ids['button_duration_dropdown']
            self.duration_dropdown.bind_button(main_button=button_duration)

            # service dropdown
            button_service = self.ids['button_service_dropdown']
            self.service_dropdown.bind_button(main_button=button_service)

            # dogsDataTable
            dogsDataTable = self.ids['dogsDataTable']
            dogsDataTable.bind(is_row_selected=self.setter('is_dog_selected'))
            dogsDataTable.bind(object_selected=self.setter('dog_selected'))

            self.everything_bound = True

        # reset to default if self.reset==True
        self.set_widgets()

    def accept_button_click(self):
        if self.adding:
            self.add_appoint()
        else:
            self.edit_appoint()

    def set_widgets(self):
        # adding appointment
        if self.adding:
            self.title_label_text = 'Dodawanie wizyty'
            self.accept_button_text = 'Dodaj'
            # should you reset all fields
            if self.reset:
                self.ids['status_label'].reset_to_default()
                self.owner = None
                self.hour_dropdown.update_main_button(obj='12')
                self.min_dropdown.update_main_button(obj='0')
                self.duration_dropdown.update_main_button(obj=datetime.timedelta(minutes=45))
                self.service_dropdown.list_objects = []
                self.service_dropdown.list_objects = app.controller.get_services()
                self.service_dropdown.update_main_button(obj=Service(id=None, name="Wybierz serwis"))
                self.ids['txt_input_cost'].text = ''
        # editing appointment
        else:
            self.title_label_text = 'Edytowanie wizyty'
            self.accept_button_text = 'Zapisz'
            if self.reset:
                self.day = self.appoint_edited.date.date()
                self.owner = self.appoint_edited.dog.owner
                self.ids['dogsDataTable'].obj_select(self.appoint_edited.dog)
                self.hour_dropdown.update_main_button(obj=self.appoint_edited.date.strftime('%H'))
                self.min_dropdown.update_main_button(obj=self.appoint_edited.date.strftime('%M'))
                self.duration_dropdown.update_main_button(obj=self.appoint_edited.time)
                self.service_dropdown.list_objects = []
                self.service_dropdown.list_objects = app.controller.get_services()
                self.service_dropdown.update_main_button(obj=self.appoint_edited.service)
                self.ids['txt_input_cost'].text = '{:.0f}'.format(self.appoint_edited.cost)
        if not self.reset:
            self.reset = True

            # update dogs after leaving
            was_dog_selected = self.is_dog_selected
            dog_selected = self.dog_selected
            # reset dogsDataTable
            owner = self.owner
            self.owner = None
            self.owner = owner
            # update dogs after changes
            if was_dog_selected:
                self.ids['dogsDataTable'].obj_select(dog_selected)
        else:
            self.accept_button_disabled = False
            self.ids['status_label'].reset_to_default()

    def on_day(self, instance, value: datetime.date):
        self.day_button_text = '{} {}'.format(value.strftime("%d"),
                                              translations.genitive_months_names[int(value.strftime("%m"))])

    def on_owner(self, instance, value: Owner):
        if value is not None:
            if value.phone_name is not None:
                self.owner_button_text = '{}(numer: {})'.format(value.phone_name, value.phone_number)
            else:
                self.owner_button_text = 'numer: {}'.format(value.phone_number)
            self.ids['dogsDataTable'].list_objects = app.controller.get_dogs(owner=value)
        else:
            self.owner_button_text = ''
            self.ids['dogsDataTable'].list_objects = []

    def add_appoint(self):
        dog = self.dog_selected
        service = self.service_dropdown.main_button.obj
        date = datetime.datetime(year=self.day.year, month=self.day.month, day=self.day.day,
                                 hour=int(self.hour_dropdown.main_button.obj),
                                 minute=int(self.min_dropdown.main_button.obj))
        time = self.duration_dropdown.main_button.obj
        if self.ids['txt_input_cost'].text != '':
            cost = Decimal(self.ids['txt_input_cost'].text)
        else:
            cost = Decimal(0)
        new_appoint = Appointment(id=None, dog=dog, service=service, date=date, time=time, cost=cost)


        self.ids['status_label'].text = 'Dodawanie...'
        app.controller.add_appointment(new_appoint)
        self.accept_button_disabled = True
        self.ids['status_label'].text = 'Dodano wizytę'

        self.ids['status_label'].change_color((191 / 255, 64 / 255, 191 / 255, 1))

    def edit_appoint(self):
        dog = self.dog_selected
        service = self.service_dropdown.main_button.obj
        date = datetime.datetime(year=self.day.year, month=self.day.month, day=self.day.day,
                                 hour=int(self.hour_dropdown.main_button.obj),
                                 minute=int(self.min_dropdown.main_button.obj))
        time = self.duration_dropdown.main_button.obj
        if self.ids['txt_input_cost'].text != '':
            cost = Decimal(self.ids['txt_input_cost'].text)
        else:
            cost = Decimal(0)

        edited_appoint = Appointment(id=self.appoint_edited.id, dog=dog, service=service, date=date, time=time, cost=cost)

        self.ids['status_label'].text = 'Edytowanie...'
        self.appoint_edited = app.controller.edit_appointment(edited_appoint)
        self.ids['status_label'].text = 'Edytowano'

        self.ids['status_label'].change_color((191 / 255, 64 / 255, 191 / 255, 1))

    @staticmethod
    def timedelta_to_str(timedelta: datetime.timedelta):
        hrs = int(timedelta.total_seconds() // 3600)
        mins = int((timedelta.total_seconds() - 3600 * hrs) / 60)
        if hrs == 0:
            return '{} min'.format(str(mins))
        else:
            return '{} h {} min'.format(str(hrs), str(mins))
