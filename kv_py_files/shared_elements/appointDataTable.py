from kivy.metrics import dp

from entities.appointment import Appointment
from kv_py_files.shared_elements.myDataTable import MyDataTable


class AppointDataTable(MyDataTable):

    def __init__(self, **kwargs):
        super().__init__(bg_color=(220/255, 220/255, 220/255, 1),
                         selected_color=(0, 220/255, 220/255, 1),
                         not_selected_color=(220/255, 220/255, 220/255, 1),
                         main_row_color=(190 / 255, 190 / 255, 190 / 255, 1),
                         font_color=(0, 0, 0, 1),
                         height_row=dp(30),
                         columns_names=('godzina', 'nazwa w tel', 'nazwisko', 'rasa'),
                         columns_funcs=(self.get_hour, self.get_phone_name, self.get_last_name, self.get_breed),
                         columns_widths=(4/18, 5/18, 3/18, 6/18),
                         **kwargs)

    @staticmethod
    def get_hour(appoint: Appointment):
        return appoint.date.strftime("%H:%M")

    @staticmethod
    def get_phone_name(appoint:Appointment):
        return AppointDataTable.filter_none(appoint.dog.owner.phone_name)

    @staticmethod
    def get_last_name(appoint: Appointment):
        return AppointDataTable.filter_none(appoint.dog.owner.last_name)

    @staticmethod
    def get_breed(appoint: Appointment):
        return AppointDataTable.filter_none(appoint.dog.breed.name)

    @staticmethod
    def filter_none(obj):
        if obj is None:
            return ''
        return obj