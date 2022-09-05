from kivy.uix.screenmanager import Screen

import datetime

class EditDayScreen(Screen):
    day: datetime.date

    def on_pre_enter(self, *args):
        print(self.day)
