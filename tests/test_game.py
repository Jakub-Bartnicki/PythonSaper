import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import pytest
from kivy.core.window import Window
from gameplay.boardlayout import BoardLayout
from gameplay.game import Game


@pytest.fixture
def boardLayout():
    '''Returns new Board Layout with board size equals 1 and with 6 bombs'''
    boardLayout = BoardLayout()
    boardLayout.createBoard(3, 2)
    return boardLayout


# choose easy level
def test_setEasyLevel():
    game = Game()
    game.setEasyLevel()
    
    assert game.boardLayout.boardSize == 8 and game.boardLayout.bombsAmount == 6


# choose normal level
def test_setNormalLevel():
    game = Game()
    game.setNormalLevel()
    
    assert game.boardLayout.boardSize == 12 and game.boardLayout.bombsAmount == 12


# choose hard level
def test_setHardLevel():
    game = Game()
    game.setHardLevel()
    
    assert game.boardLayout.boardSize == 16 and game.boardLayout.bombsAmount == 26


# choose expert level
def test_setExpertLevel():
    game = Game()
    game.setExpertLevel()
    
    assert game.boardLayout.boardSize == 20 and game.boardLayout.bombsAmount == 40


# set window size
def test_setWindowSize(boardLayout):
    game = Game()
    game.boardLayout = boardLayout
    size = game.boardLayout.boardSize * 30

    game.setWindowSize()

    assert Window.size == (90, 108)