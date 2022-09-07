import datetime

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen


class AddAppointScreen(Screen):
    day: datetime.date
    day_str = StringProperty()

    def on_pre_enter(self, *args):
        self.day_str = self.day.strftime("%m/%d")
        print(self.day)
