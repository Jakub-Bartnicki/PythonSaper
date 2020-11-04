from random import randrange
import kivy
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.app import App



class BoardLayout(GridLayout):
    def __init__(self, **kwargs):
        super(BoardLayout, self).__init__(**kwargs)
        self.mouse = "left"

        self.board = []
        
    # add bombs
    def addBombs(self):
        bombList = []
        added = False
        for i in range(0, self.bombsAmount):
            bombId = randrange(0, self.boardSize*self.boardSize)
            while bombId in bombList:
                bombId = randrange(0, self.boardSize*self.boardSize)
            for squareList in self.board:
                for square in squareList:
                    if square.id == str(bombId):
                        bombList.append(bombId)
                        added = True
                        break
                if added:
                    added = False
                    break
        return bombList

    # add flag
    def addFlag(self, instance):
        if instance.text == "":
            instance.text = "F"  
        else:  
            instance.text = ""  

    # create squares
    def createBoard(self, boardSize = 6, bombsAmount = 1):
        self.board.clear()
        self.clear_widgets()
        self.boardSize = boardSize
        self.bombsAmount = bombsAmount
        self.cols = boardSize
        self.rows = boardSize

        box = []
        for i in range(0, boardSize):
            box.append([])
            for j in range(0, boardSize):
                box[i].append(Button(id = str(i * boardSize + j), text = "", size_hint_y = 1/boardSize, size_hint_x = 1/boardSize, font_size = 24))
                box[i][j].bind(on_release = self.onPressed)
                self.add_widget(box[i][j])

        self.uncoveredSquaresList = set()
        self.board = box
        self.bombList = self.addBombs()

    # disable squares with bombs after win
    def disableSquares(self):
        for squareList in self.board:
            for square in squareList:
                if square.disabled == False:
                    square.disabled = True
                    square.background_color = [3.4, 3.4, 3.4, 10]
                    square.color = [6, 6, 6, 10]

    # win/lose, changes 'play' button color
    def gameResult(self, result = None):
        # if win
        if len(self.uncoveredSquaresList) == self.boardSize * self.boardSize - self.bombsAmount:
            self.disableSquares()
            app = App.get_running_app()
            app.root.ids['play'].background_color = [0, 1, 0, 1]
        # if lose
        elif len(self.uncoveredSquaresList) > 0 and result == "lose":
            self.disableSquares()
            self.revealBombs()
            app = App.get_running_app()
            app.root.ids['play'].background_color = [1, 0, 0, 1]
            

    # found bomb
    def hasBomb(self, id):
        if int(id) in self.bombList:
            return True
        return False

    # when clicked
    def onPressed(self, instance):
        if self.mouse == 'right':
            self.addFlag(instance)
        if self.mouse == 'left':
            self.revealSquare(instance)

    # write amount of near bombs
    def howMuchBombs(self, instance):
        bombs = 0

        nearSquares = self.nearSquares(instance.id)
        for square in nearSquares:
            if self.hasBomb(square.id):
                bombs += 1

        if bombs != 0:
            instance.text = str(bombs)
        return bombs

    # returns squares near square with exact id
    def nearSquares(self, id):
        nears = []
        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                actualId = i * self.boardSize + j
                squareId = int(id)
                # top
                if actualId + self.boardSize == squareId:
                    nears.append(self.board[i][j])
                # left
                elif actualId + 1 == squareId and actualId % self.boardSize != self.boardSize - 1:
                    nears.append(self.board[i][j])
                # right
                elif actualId - 1 == squareId and actualId % self.boardSize != 0:
                    nears.append(self.board[i][j])
                # bottom
                elif actualId - self.boardSize == squareId:
                    nears.append(self.board[i][j])
                # top left
                elif actualId + self.boardSize + 1 == squareId and actualId % self.boardSize != self.boardSize - 1:
                    nears.append(self.board[i][j])
                # top right
                elif actualId + self.boardSize - 1 == squareId and actualId % self.boardSize != 0:
                    nears.append(self.board[i][j])
                # bottom left
                elif actualId - self.boardSize + 1 == squareId and actualId % self.boardSize != self.boardSize - 1:
                    nears.append(self.board[i][j])
                # bottom right
                elif actualId - self.boardSize - 1 == squareId and actualId % self.boardSize != 0:
                    nears.append(self.board[i][j])
        return nears

    # reveal all bombs
    def revealBombs(self):
        for squareList in self.board:
            for square in squareList:
                if self.hasBomb(square.id):
                    square.disabled = True
                    square.text = "*"
                    square.background_color = (6, 0, 0, 10)
                    square.color = [6, 6, 6, 10]

    # reveal square
    def revealSquare(self, instance):
        if not self.hasBomb(instance.id):
            self.uncoveredSquaresList.add(instance)
            instance.disabled = True
            instance.background_color = [6, 6, 6, 10]
            instance.color = [6, 6, 6, 10]
            nearSquares = self.nearSquares(instance.id)
            if self.howMuchBombs(instance) == 0:
                for square in nearSquares:  
                    if square.disabled == False:
                        self.revealSquare(square)
            self.gameResult()
        else:
            self.gameResult("lose")
            
    # self.mouse means which button (left/right) was clicked
    def on_touch_down(self, touch):
        self.mouse = touch.button
        return super().on_touch_down(touch)
