import datetime
from decimal import Decimal

from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.screenmanager import Screen

from controller import translations
from controller.errors import InsertAppointmentError
from entities.appointment import Appointment
from entities.owner import Owner
from entities.service import Service
from kv_py_files.dogsApp import app
from kv_py_files.shared_elements.myDropDown import MyDropDown


class AddAppointScreen(Screen):
    day: datetime.date

    # date
    day_str = StringProperty()

    # time selection
    hour_dropdown: MyDropDown
    hours_displayed = [str(i) for i in range(7, 22)]
    min_dropdown: MyDropDown
    mins_displayed = [str(i) for i in range(0, 61, 5)]

    # service selection
    service_dropdown: MyDropDown

    # time selection
    duration_dropdown: MyDropDown
    durations_displayed = [datetime.timedelta(minutes=m)
                           for m in (15, 20, 25, 30, 40, 45, 50, 60, 70, 75, 80, 90, 105, 120)]

    # selectOwner
    owner = ObjectProperty(None, allownone=True)
    owner_str = StringProperty()

    # dogsDataTable
    is_dog_selected = BooleanProperty(False)
    dog_selected = ObjectProperty(None, allownone=True)

    reset = True

    # after initialization this will be True
    everything_bound: bool = False
    has_already_added = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # time dropdowns
        self.hour_dropdown = MyDropDown(height_row=dp(25), btn_color=(220/255, 220/255, 220/255, 1), attr_name=None)
        self.min_dropdown = MyDropDown(height_row=dp(25), btn_color=(220/255, 220/255, 220/255, 1), attr_name=None)

        self.hour_dropdown.list_objects = self.hours_displayed
        self.min_dropdown.list_objects = self.mins_displayed

        # time dropdown
        self.duration_dropdown = MyDropDown(height_row=dp(25), btn_color=(220/255, 220/255, 220/255, 1),
                                            attr_name=None, attr_func=self.timedelta_to_str)
        self.duration_dropdown.list_objects = self.durations_displayed

        # service dropdown
        self.service_dropdown = MyDropDown(height_row=dp(25), btn_color=(220/255, 220/255, 220/255, 1), attr_name='name')



    def on_pre_enter(self, *args):
        self.day_str = '{} {}'.format(self.day.strftime("%d"),
                                      translations.genitive_months_names[int(self.day.strftime("%m"))])

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

        # reset to default
        if not self.reset:
            self.reset = True
        else:
            self.owner = None
            self.hour_dropdown.update_main_button(obj='12')
            self.min_dropdown.update_main_button(obj='00')
            self.duration_dropdown.update_main_button(obj=datetime.timedelta(minutes=45))
            self.service_dropdown.list_objects = []
            self.service_dropdown.list_objects = app.controller.get_services()
            self.service_dropdown.update_main_button(obj=Service(id=None, name="Wybierz serwis", appointments=None))
            self.ids['txt_input_cost'].text = ''
            self.ids['status_label'].reset_to_default()
            self.has_already_added = False

    def on_owner(self, instance, value: Owner):
        if value is not None:
            self.owner_str = 'numer: {}, nazwa: {}, nazwisko: {}'.format(value.phone_number,
                                                                     value.phone_name, value.last_name)
            self.ids['dogsDataTable'].list_objects = value.dogs
        else:
            self.owner_str = ''
            self.ids['dogsDataTable'].list_objects = []

    def add_button_click(self):

        dog = self.dog_selected
        service = self.service_dropdown.main_button.obj
        date = datetime.datetime(year=self.day.year, month=self.day.month, day=self.day.day,
                                 hour=int(self.hour_dropdown.main_button.obj),
                                 minute=int(self.min_dropdown.main_button.obj))
        time = self.duration_dropdown.main_button.obj
        cost = Decimal(int(self.ids['txt_input_cost'].text))
        new_appoint = Appointment(id=None, dog=dog, service=service, date=date, time=time, cost=cost)

        try:
            self.ids['status_label'].text = 'Dodawanie...'
            app.controller.add_appointment(new_appoint)
            self.has_already_added = True
            self.ids['status_label'].text = 'Dodano wizytę'
        except InsertAppointmentError as err:
            print(err.sql_error)
            self.ids['status_label'].text = err.msg
        self.ids['status_label'].change_color((191 / 255, 64 / 255, 191 / 255, 1))

    @staticmethod
    def timedelta_to_str(timedelta: datetime.timedelta):
        hrs = int(timedelta.total_seconds() // 3600)
        mins = int((timedelta.total_seconds() - 3600*hrs) / 60)
        if hrs == 0:
            return '{} min'.format(str(mins))
        else:
            return '{} h {} min'.format(str(hrs), str(mins))

