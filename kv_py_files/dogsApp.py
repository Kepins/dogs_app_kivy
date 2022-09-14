from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp

from controller.controller import Controller
from kivy.config import Config

from controller.errors import ConnectError


class DogsApp(App):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.controller = Controller()
            self.kv_file = './kv_files/main.kv'
        except ConnectError as err:
            self.kv_file = './kv_files/connectError.kv'

    def build(self):
        Config.set('graphics', 'width', '1280')
        Config.set('graphics', 'height', '720')
        Config.write()

        kv = Builder.load_file(self.kv_file)
        return kv


app = DogsApp()
