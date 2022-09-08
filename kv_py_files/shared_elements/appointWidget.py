import datetime

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from entities.appointment import Appointment


class AppointWidget(BoxLayout):
    font_size = dp(12)
    font_color = (0.1, 0.1, 0.1, 1)

    def __init__(self, appoint: Appointment, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, None)
        self.height = dp(40)

        time_label = Label(font_size=self.font_size, color=self.font_color)
        finish_time = appoint.date + appoint.time
        time_label.text = '{} - {}'.format(appoint.date.strftime("%H:%M"), finish_time.strftime("%H:%M"))
        self.add_widget(time_label)
        second_label = Label(font_size=self.font_size, color=self.font_color)
        if appoint.dog.owner.phone_name is not None:
            second_label.text = appoint.dog.owner.phone_name
        else:
            second_label.text = appoint.dog.owner.phone_number
        self.add_widget(second_label)
        self.add_widget(Widget())
