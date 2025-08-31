from enum import Enum
import numpy as np


class Team(Enum):
    noughts = 0
    crosses = 1


class Game:

    # special methods:

    def __init__(self, state=None, n=3):
        # config:
        self.n = n
        self.n_teams = 2
        self.symbols = {
            Team.noughts: 'o',
            Team.crosses: 'x'
        }

        # convenience:
        self._nought = self.symbols[Team.noughts]
        self._cross = self.symbols[Team.crosses]

        # init:
        self.state = np.array(state) if state else np.array([[' '] * n] * n, dtype=str)
        self.turn = 0   # can be overridden by self._validate()
        self.moves = 0  # ^
        self._validate()

        # final state:
        self.winner: Team = self._find_winner()
        self.win_reason: str = None

    def __str__(self):
        return str(self.state)
    
    # private methods:

    def _validate(self):
        """
        Called upon game creation to ensure parameters are consistent with custom game state.
        """
        occupied = []
        n_noughts = 0
        n_crosses = 0

        for row in range(self.n):
            for col in range(self.n):
                cell = (row, col)
                if not self.empty_cell(cell):
                    occupied.append(cell)

        for cell in occupied:
            sym = self.state[cell]
            n_noughts += 1 if sym == self._nought else 0
            n_crosses += 1 if sym == self._cross else 0

        if n_crosses > n_noughts or n_noughts - n_crosses > 1:
            raise RuntimeError("invalid state")
        
        self.moves = len(occupied)
        self._refresh()
    
    def _find_winner(self) -> Team | None:
        noughts_winner = self._has_won(Team.noughts)
        crosses_winner = self._has_won(Team.crosses)

        if noughts_winner:
            return Team.noughts
        if crosses_winner:
            return Team.crosses
        
        return None

    def _has_won(self, team: Team) -> bool:
        """
        Checks for a line that has 3 of the symbol associated with the given `team`.

        Args:
            team (Team): Team for which a win is being checked.

        Returns:
            bool: Whether that team won.
        """

        lines = self.get_lines()

        for line in lines:
            if np.all([c == self.symbols[team] for c in line]):
                return True
            
        return False
    
    def _refresh(self):
        """
        Update parameters.
        """

        self.winner = self._find_winner()
        self.turn = np.mod(self.moves, self.n_teams)
                
    def _update(self, pos, sym):
        """Handles placement logic.

        Args:
            pos (tuple): Position to place symbol.
            sym (str): Symbol to place on grid.
        """

        x, y = pos
        # ensure game isn't already over:
        if self.winner is not None:
            raise RuntimeError(f"game is over ({self.winner.name} won)")
        # ensure inputs are valid:
        if not (isinstance(x, int) and isinstance(y, int)):
            raise RuntimeError(f"coordinate must only contain valid integers: ({x}, {y})")
        # ensure coordinates are in bounds:
        if not ((0 <= x < self.n) and (0 <= y < self.n)):
            raise RuntimeError(f"coordinates are not valid: ({x}, {y})")
        # ensure cell-to-write is empty:
        if not self.empty_cell(pos):
            raise RuntimeError("cell is not free")
        
        self.state[pos] = sym
        self.moves += 1
        self._refresh()

        if self.winner:
            print(f"game is over: {self.winner} won")

    # public methods:
    
    def empty_cell(self, pos) -> bool:
        """
        Convenience method to determine whether a cell is unoccupied.

        Args:
            pos (tuple): Coordinate of cell.

        Returns:
            bool: Whether cell is unoccupied.
        """

        return self.state[pos] == ' '
    
    def get_lines(self) -> list[np.ndarray]:
        """
        Returns list of 3-length arrays describing each row, column and diagonal.

        Returns:
            list[np.ndarray]: List of arrays containing each row, column and diagonal.
        """

        diag = np.diag(self.state)
        adiag = np.diag(np.flipud(self.state))
        rows = []
        cols = []

        for i in range(self.n):
            rows.append(self.state[i, :])
            cols.append(self.state[:, i])

        return diag, adiag, *rows, *cols

    def play(self, x, y):
        team = list(Team)[self.turn]
        self._update((x, y), self.symbols[team])