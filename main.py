from kivy.app import App
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


# Define different screens
class WelcomeScreen(Screen):
    pass


class ClientsScreen(Screen):
    pass


class AddClientScreen(Screen):
    def on_add_button_click(self):
        phone_number = self.ids.txt_input_phone_number.text
        first_name = self.ids.txt_input_first_name.text
        last_name = self.ids.txt_input_last_name.text

        print('phone: {}\nfirst name: {}\nlast name: {}'.format(phone_number, first_name, last_name))


class EditClientScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class ClientsDataTable(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        columns = ['telefon', 'imię', 'nazwisko']
        height_row = dp(30)

        main_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=height_row)
        widths = [0.4, 0.3, 0.3]
        for column, width in zip(columns, widths):
            label = Label(text=column, size_hint=(width, 1))
            main_row.add_widget(label)
        self.add_widget(main_row)

        # testing purposes
        customers = [('231321321', 'Adam', 'Kow'), ('721213933', 'Szymon', 'Now'),('721313933', 'Jan', 'Podolski')]*3

        scrollView = ScrollView()
        gridLayout = GridLayout()
        gridLayout.cols = 1
        gridLayout.size_hint = (1, None)
        gridLayout.bind(minimum_height=gridLayout.setter('height'))
        for customer in customers:
            row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=height_row)
            for prop, width in zip(customer, widths):
                label = Label(text=prop, size_hint=(width, 1))
                row.add_widget(label)
            gridLayout.add_widget(row)
        scrollView.add_widget(gridLayout)
        self.add_widget(scrollView)


class DogsApp(App):
    pass


if __name__ == '__main__':
    DogsApp().run()
