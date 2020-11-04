import kivy
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from gameplay.boardlayout import BoardLayout
from gameplay.level import Level


class Game(GridLayout):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)    
        self.cols = 1
        self.rows = 2

        self.boardLayout = BoardLayout()
        self.popupWindow = Popup(title="Choose Level", title_align="center", content = Level(), size_hint=(0.8, 0.8))
        self.add_widget(self.boardLayout)

    # choose easy level
    def setEasyLevel(self):
        self.boardLayout.createBoard(8, 6)
        self.setWindowSize()

    # choose normal level
    def setNormalLevel(self):
        self.boardLayout.createBoard(12, 12)
        self.setWindowSize()

    # choose hard level
    def setHardLevel(self):
        self.boardLayout.createBoard(16, 26)
        self.setWindowSize()

    # choose expert level
    def setExpertLevel(self):
        self.boardLayout.createBoard(20, 40)
        self.setWindowSize()

    # set window size
    def setWindowSize(self):
        size = self.boardLayout.boardSize * 30
        Window.size = (size, size * 1.2)
        self.popupWindow.dismiss()

    # show popup with game settings
    def showPopup(self):
        self.popupWindow.open()
        