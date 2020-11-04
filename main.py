from kivy.config import Config
Config.set('graphics', 'width', 400)
Config.set('graphics', 'height', 500)
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,disable_multitouch')
import kivy
from kivy.app import App
from gameplay.game import Game


class MainApp(App):
    def build(self):
        game = Game()

        return game

if __name__ == "__main__":
    MainApp().run()
