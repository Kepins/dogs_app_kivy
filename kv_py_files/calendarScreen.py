import datetime
import calendar

from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

from kv_py_files.shared_elements.dayCalendar import DayCalendar


class CalendarScreen(Screen):
    year: int
    month: int
    title_text = StringProperty()
    __months_in_polish = {
        1: 'styczeń',
        2: 'luty',
        3: 'marzec',
        4: 'kwiecień',
        5: 'maj',
        6: 'czerwiec',
        7: 'lipiec',
        8: 'sierpień',
        9: 'wrzesień',
        10: 'październik',
        11: 'listopad',
        12: 'grudzień'
    }
    today_bg_color = (210/255, 222/255, 250/255, 1)
    day_bg_colors = ((220/255, 220/255, 220/255, 1), (215/255, 215/255, 215/255, 1))


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.year = datetime.date.today().year
        # self.month = datetime.date.today().month
        self.year = 2022
        self.month = 6

    def on_pre_enter(self, *args):
        self.title_text = self.__months_in_polish[self.month]
        self.load_days()

    def load_days(self):
        gridLayout = self.ids['calendarGrid']
        gridLayout.clear_widgets()

        days_to_display = self.calculate_days_to_display()

        color = 0
        for day in days_to_display:
            dayCalendar = DayCalendar(bg_color=self.day_bg_colors[color%2], day=day)
            if day == datetime.date.today():
                dayCalendar.change_color(bg_color=self.today_bg_color)
            gridLayout.add_widget(dayCalendar)

            color+=1

    def calculate_days_to_display(self):
        month_first_day = datetime.date(year=self.year, month=self.month, day=1)
        first_day_display = month_first_day + datetime.timedelta(days=-month_first_day.weekday())
        days = []
        for i in range(35):
            days.append(first_day_display + datetime.timedelta(days=i))
        return days
