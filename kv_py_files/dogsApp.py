from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp

from controller.controller import Controller
from kivy.config import Config




class DogsApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = Controller()
        self.file_to_load = './kv_files/main.kv'

    def build(self):
        Config.set('graphics', 'width', '1280')
        Config.set('graphics', 'height', '720')
        Config.write()

        kv = Builder.load_file(self.file_to_load)
        return kv


app = DogsApp()
