from kivy.graphics import Color
from kivy.metrics import dp
from kivy.uix.label import Label

from entities.appointment import Appointment


class AppointLabel(Label):
    def __init__(self, appoint: Appointment, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = dp(12)
        self.font_size = dp(12)
        self.color = (0.1, 0.1, 0.1, 1)
        self.text = '{t} {phone}'.format(t=appoint.date.strftime("%H:%M"), phone=appoint.dog.owner.phone_name)
