# should be used in ClientsDataTable, DogsDataTable
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout


class ClickableBoxLayout(ButtonBehavior, BoxLayout):
    def __init__(self, bg_color, **kwargs):
        # make sure we aren't overriding any important functionality
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(rgba=bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def change_color(self, bg_color):
        with self.canvas.before:
            Color(rgba=bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)