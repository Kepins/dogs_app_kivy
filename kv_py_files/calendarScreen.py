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
    today_bg_color = (190/255, 202/255, 230/255, 1)
    day_bg_colors = ((210/255, 210/255, 210/255, 1), (205/255, 205/255, 205/255, 1))


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month


    def on_pre_enter(self, *args):
        self.title_text = self.__months_in_polish[self.month] + ' ' + str(self.year)
        self.load_days()

    def load_days(self):
        gridLayout = self.ids['calendarGrid']
        gridLayout.clear_widgets()

        days_to_display = self.calculate_days_to_display()

        color = 0
        for day in days_to_display:
            bg_color = self.day_bg_colors[color % 2]
            if day == datetime.date.today():
                bg_color = self.today_bg_color
            if day.month != self.month:
                bg_color = self.dim_color(bg_color)

            dayCalendar = DayCalendar(bg_color=bg_color, day=day)
            gridLayout.add_widget(dayCalendar)

            color+=1

    def calculate_days_to_display(self):
        month_first_day = datetime.date(year=self.year, month=self.month, day=1)
        first_day_display = month_first_day + datetime.timedelta(days=-month_first_day.weekday())
        days = []
        for i in range(42):
            days.append(first_day_display + datetime.timedelta(days=i))
        return days

    def on_next_month(self):
        if self.month + 1 > 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.on_pre_enter()

    def on_prev_month(self):
        if self.month - 1 == 0:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.on_pre_enter()

    @staticmethod
    def dim_color(color):
        dimmed_color = [color[0]-25/255, color[1]-25/255, color[2]-25/255, color[3]]
        for i in range(len(dimmed_color)):
            if dimmed_color[i] < 0:
                dimmed_color[i] = 0
            elif dimmed_color[i] > 1:
                dimmed_color[i] = 1
        return dimmed_color
