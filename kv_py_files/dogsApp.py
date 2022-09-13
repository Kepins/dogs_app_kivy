from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp

from controller.controller import Controller
from kivy.config import Config

class DogsApp(App):
    controller = Controller()

    def build(self):
        Config.set('graphics', 'width', '1280')
        Config.set('graphics', 'height', '720')
        Config.write()

        kv = Builder.load_file('./kv_files/main.kv')
        return kv


app = DogsApp()
