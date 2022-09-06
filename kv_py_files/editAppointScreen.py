from kivy.uix.screenmanager import Screen

from entities.appointment import Appointment


class EditAppointScreen(Screen):
    appoint: Appointment

    def on_pre_enter(self, *args):
        print(self.appoint)
