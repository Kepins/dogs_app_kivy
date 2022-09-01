from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label


class StatusLabel(Label):
    default_color = (240/255, 240/255, 240/255, 1)

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=self.default_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def change_color(self, bg_color):
        with self.canvas.before:
            Color(rgba=bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def reset_to_default(self):
        self.text = ''
        self.change_color(self.default_color)
