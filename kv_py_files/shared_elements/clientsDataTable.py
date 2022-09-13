from kivy.metrics import dp

from entities.owner import Owner
from kv_py_files.shared_elements.myDataTable import MyDataTable


class ClientsDataTable(MyDataTable):

    def __init__(self, **kwargs):
        super().__init__(bg_color=(220/255, 220/255, 220/255, 1),
                         selected_color=(0, 220/255, 220/255, 1),
                         not_selected_color=(220/255, 220/255, 220/255, 1),
                         main_row_color=(190 / 255, 190 / 255, 190 / 255, 1),
                         font_color=(0, 0, 0, 1),
                         height_row=dp(30),
                         columns_names=('telefon', 'nazwa w tel', 'imię', 'nazwisko', 'notka'),
                         columns_funcs=(self.get_phone_number, self.get_phone_name,
                                        self.get_last_name, self.get_last_name, self.get_note),
                         columns_widths=(4/24, 6/24, 4/24, 4/24, 6/24),
                         **kwargs)

    @staticmethod
    def get_phone_number(owner: Owner):
        return owner.phone_number

    @staticmethod
    def get_phone_name(owner: Owner):
        return ClientsDataTable.filter_none(owner.phone_name)

    @staticmethod
    def get_first_name(owner: Owner):
        return ClientsDataTable.filter_none(owner.first_name)

    @staticmethod
    def get_last_name(owner: Owner):
        return ClientsDataTable.filter_none(owner.last_name)

    @staticmethod
    def get_note(owner: Owner):
        return ClientsDataTable.filter_none(owner.note)

    @staticmethod
    def filter_none(obj):
        if obj is None:
            return ''
        return obj
