from kivy.metrics import dp

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
                         attr_names=('date', 'dog.owner.phone_name', 'dog.owner.last_name', 'dog.breed.name'),
                         attr_func=(lambda d: d.strftime("%H:%M"), super().check_none, super().check_none, super().check_none),
                         columns_widths=(4/18, 5/18, 3/18, 6/18),
                         **kwargs)
