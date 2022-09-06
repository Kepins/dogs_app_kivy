from kivy.metrics import dp

from kv_py_files.shared_elements.myDataTable import MyDataTable


class ClientsDataTable(MyDataTable):

    def __init__(self, **kwargs):
        super().__init__(bg_color=(220/255, 220/255, 220/255, 1),
                         selected_color=(0, 220/255, 220/255, 1),
                         not_selected_color=(220/255, 220/255, 220/255, 1),
                         height_row=dp(30),
                         columns_names=('telefon', 'imię', 'nazwisko', 'notka'),
                         attr_names=('phone', 'first_name', 'last_name', 'note'),
                         columns_widths=(4/18, 4/18, 4/18, 6/18),
                         **kwargs)
