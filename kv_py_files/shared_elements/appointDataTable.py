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
                         columns_names=('godzina', 'nazwa w tel', 'rasa psa', 'koszt'),
                         columns_funcs=(self.get_time, self.get_phone_name, self.get_breed, self.get_cost),
                         columns_widths=(3/18, 6/18, 7/18, 2/18),
                         **kwargs)

    @staticmethod
    def get_time(appoint: Appointment):
        finish_time = appoint.date + appoint.time
        text = '{} - {}'.format(appoint.date.strftime("%H:%M"), finish_time.strftime("%H:%M"))
        return text

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
    def get_cost(appoint: Appointment):
        return '{:.2f}'.format(appoint.cost)

    @staticmethod
    def filter_none(obj):
        if obj is None:
            return ''
        return obj