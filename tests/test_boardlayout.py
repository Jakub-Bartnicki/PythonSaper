import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import pytest
from gameplay.boardlayout import BoardLayout
from kivy.uix.button import Button

@pytest.fixture
def boardLayout():
    '''Returns new Board Layout with board size equals 1 and with 6 bombs'''
    boardLayout = BoardLayout()
    boardLayout.createBoard(3, 2)
    return boardLayout


# add bombs to game board
def test_addBombs(boardLayout):
    bombList = boardLayout.addBombs()

    assert len(bombList) == 2


# add flag to exact square
def test_addFlag(boardLayout):
    square = boardLayout.board[0][0]
    square.text = ""

    boardLayout.addFlag(square)

    assert square.text == "F"


# is creating array of buttons
def test_createBoard():
    newBoardLayout = BoardLayout()
    bombsAmount = 2
    boardSize = 3

    newBoardLayout.createBoard(boardSize, bombsAmount)
    amountOfSquares = len(newBoardLayout.board) * len(newBoardLayout.board[0])

    assert amountOfSquares == boardSize*boardSize and isinstance(newBoardLayout.board[0][0], Button)
        

# found bomb
def test_hasBomb():
    bombList = [1, 4, 6]
    newBoardLayout = BoardLayout()
    newBoardLayout.bombList = bombList

    result = newBoardLayout.hasBomb(1)
    
    assert result


# returns amount of near bombs
def test_howMuchBombs(boardLayout):
    boardLayout.bombsAmount = 4
    boardLayout.bombList = [0, 3, 5, 7]
    
    assert boardLayout.howMuchBombs(boardLayout.board[1][1]) == 4


# returns squares near square with exact id
def test_nearSquares(boardLayout):
    board = boardLayout.board
    assumedNearSquaresList = [board[0][0], board[0][1], board[0][2], board[1][0], board[1][2], board[2][0], board[2][1], board[2][2]]

    assert boardLayout.nearSquares(4) == assumedNearSquaresList


# reveal all bombs
def test_revealBombs(boardLayout):
    boardLayout.bombsAmount = 2
    boardLayout.bombList = [0, 5]

    boardLayout.revealBombs()
    board = boardLayout.board

    assert board[1][2].text == "*" and board[0][0].text == "*" and board[0][1].text == ""


# reveal square
def test_revealSquare(boardLayout):
    boardLayout.bombsAmount = 2
    boardLayout.bombList = [0, 2]

    board = boardLayout.board
    uncoveredSquares = {board[2][2], board[2][1], board[2][0], board[1][2], board[1][1], board[1][0]}

    boardLayout.revealSquare(board[2][2])

    assert uncoveredSquares == boardLayout.uncoveredSquaresList
