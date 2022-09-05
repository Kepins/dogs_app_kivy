from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from datetime import date

from kivy.uix.widget import Widget

from kv_py_files.dogsApp import app
from kv_py_files.shared_elements.appointLabel import AppointLabel


class DayCalendar(ButtonBehavior, BoxLayout):
    day: date

    def __init__(self, bg_color, day: date, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.day = day

        # layout that displays appointments
        boxLayout = BoxLayout(orientation='vertical')
        appointments = app.controller.get_appointments(day=self.day)
        appointments = sorted(appointments, key=lambda a: a.date)
        for appoint in appointments:
            label = AppointLabel(appoint=appoint)
            boxLayout.add_widget(label)
        boxLayout.add_widget(Widget())
        self.add_widget(boxLayout)

        # label that displays number of the day
        day_label = Label()
        day_label.text = self.day.strftime('%d')
        day_label.size_hint = (1, None)
        day_label.height = dp(15)
        self.add_widget(day_label)

        with self.canvas.before:
            Color(rgba=bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def on_release(self):
        pass

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def change_color(self, bg_color):
        with self.canvas.before:
            Color(rgba=bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)