import datetime

from kivy.uix.screenmanager import Screen


class AddAppointScreen(Screen):
    day: datetime.date

    def on_pre_enter(self, *args):
        print(self.day)
