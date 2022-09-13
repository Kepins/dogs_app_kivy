from kivy.metrics import dp

from kv_py_files.shared_elements.myDataTable import MyDataTable


class DogsDataTable(MyDataTable):

    def __init__(self, **kwargs):
        super().__init__(bg_color=(220/255, 220/255, 220/255, 1),
                         selected_color=(0, 220/255, 220/255, 1),
                         not_selected_color=(220/255, 220/255, 220/255, 1),
                         main_row_color=(190/255, 190/255, 190/255, 1),
                         font_color=(0, 0, 0, 1),
                         height_row=dp(30),
                         columns_names=('imię', 'rasa', 'wielkość', 'notka'),
                         attr_names=('name', 'breed.name', 'size.name', 'note'),
                         columns_widths=(4/18, 5/18, 3/18, 6/18),
                         **kwargs)
