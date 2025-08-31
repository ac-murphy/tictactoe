from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from tictactoe import Game, Team
from tictactoe_ai import AIPlayer

import numpy as np
import sys


gridButtonColour = "#383838"

class MainWindow(QMainWindow):

    # special methods:

    def __init__(self, game: Game, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.game = game

        # config:
        self.n = 3

        # structure:
        self.central_widget = QWidget()
        self.grid = QGridLayout()

        # hierarchy:
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.grid)

        # generate grid:
        self.grid_buttons = np.full((self.n, self.n), None, dtype=QPushButton)
        for i in range(self.n):
            for j in range(self.n):
                self.grid_buttons[i, j] = self._newGridButton(i, j)

        # initialise AI player:
        self.AI = AIPlayer(self.game, Team.crosses)

    # private methods:

    def _newGridButton(self, x, y):
        new_button = QPushButton(' ')
        new_button.setStyleSheet(f'background:{gridButtonColour}; font-size:70px')
        new_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid.addWidget(new_button, x, y)

        new_button.clicked.connect(lambda: self._play(x, y))

        return new_button
    
    def _updateGrid(self):
        for i in range(self.n):
            for j in range(self.n):
                self.grid_buttons[i, j].setText(self.game.state[i, j])

    def _play(self, x, y):
        try:
            self.game.play(x, y)
            self._updateGrid()

            self.AI.play()
            self._updateGrid()
        except RuntimeError as e:
            print(e)

        
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()

    window = MainWindow(game)
    window.resize(800, 800)
    window.show()

    app.exec_()