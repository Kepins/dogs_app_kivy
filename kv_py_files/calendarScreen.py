import calendar
import datetime


from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

from kv_py_files.shared_elements.dayCalendar import DayCalendar
import controller.translations as translations


class CalendarScreen(Screen):
    first_day_display: datetime.date
    title_text = StringProperty()
    today_bg_color = (190/255, 202/255, 230/255, 1)
    day_bg_colors = ((210/255, 210/255, 210/255, 1), (205/255, 205/255, 205/255, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_day_display = self.get_monday(datetime.date.today())

    def on_pre_enter(self, *args):
        self.set_title()
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

            dayCalendar = DayCalendar(bg_color=bg_color, day=day)
            gridLayout.add_widget(dayCalendar)

            color+=1

    def calculate_days_to_display(self):
        days = []
        for i in range(7):
            days.append(self.first_day_display + datetime.timedelta(days=i))
        return days

    def on_next_week(self):
        self.first_day_display += datetime.timedelta(days=7)
        self.on_pre_enter()

    def on_prev_week(self):
        self.first_day_display += datetime.timedelta(days=-7)
        self.on_pre_enter()

    def set_title(self):
        first_day = self.first_day_display
        last_day = self.first_day_display + datetime.timedelta(days=6)
        if first_day.month == last_day.month:
            self.title_text = translations.months_names[first_day.month]
        else:
            self.title_text = '{}-{}'.format(translations.months_names[first_day.month],
                                             translations.months_names[last_day.month])

    # this method returns the same day if it's monday
    # else first monday before the day
    @staticmethod
    def get_monday(day: datetime.date) -> datetime.date:
        return day + datetime.timedelta(days=-day.weekday())

    # @staticmethod
    # def dim_color(color):
    #     dimmed_color = [color[0]-25/255, color[1]-25/255, color[2]-25/255, color[3]]
    #     for i in range(len(dimmed_color)):
    #         if dimmed_color[i] < 0:
    #             dimmed_color[i] = 0
    #         elif dimmed_color[i] > 1:
    #             dimmed_color[i] = 1
    #     return dimmed_color
