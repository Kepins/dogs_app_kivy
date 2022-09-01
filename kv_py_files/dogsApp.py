from kivy.app import App
from kivy.lang import Builder

from controller import Controller


class DogsApp(App):
    controller = Controller()

    def build(self):
        kv = Builder.load_file('./kv_files/main.kv')
        return kv


app = DogsApp()
