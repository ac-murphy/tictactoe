from tictactoe import Game, Team

import numpy as np
import copy


class AIPlayer:

    # special methods:

    def __init__(self, game, team: Team):
        """
        Initialise AI player.    

        Args:
            game (tictactoe.Game): Tictactoe game instance.
            player (tictactoe.Player): Team assigned (noughts or crosses).
        """

        self.game: Game = game
        self.team: Team = team

    # private methods:

    def _get_free_cells(self) -> list[tuple]:
        """
        Returns coordinates of all unoccupied cells on grid.

        Returns:
            list[tuple]: List of all unoccupied cells.
        """
        
        free = []

        for row in range(self.game.n):
            for col in range(self.game.n):
                if self.game.empty_cell((row, col)):
                    free.append((row, col))

        return free
    
    def _get_moves(self) -> tuple[list[Game], list[np.ndarray]]:
        """
        Returns all legal moves.

        Returns:
            list[Game]: List of games with next move played. \n
            list[tuple]: List of moves played in the respective game.
        """

        games = []
        moves = []

        free = self._get_free_cells()
        for x, y in free:
            new_game = copy.deepcopy(self.game)
            new_game.play(x, y)
            games.append(new_game)
            moves.append((x, y))

        return games, moves
    
    def _evaluate_state(self, game: Game) -> int:
        """
        Return integer 'score' describing how 'good' the state is.

        Args:
            game (Game): The `Game` instance.

        Returns:
            int: Score describing game state.
        """

        lines = game.get_lines()
        score = sum(self._evaluate_line(line) for line in lines)

        return score

    def _evaluate_line(self, line: np.ndarray) -> int:
        """
        Return integer 'score' describing how 'good' the line is. \n 
        _A line is one of a 'row', 'column' or 'diagonal'._

        Args:
            line (np.ndarray): Selected line from game state.

        Returns:
            int: Score describing line.
        """

        sym = self.game.symbols[self.team] 
        score = 0
        
        # scoring metric:
        for cell in line:
            if cell == sym:
                score += 2
            elif cell == ' ':
                score += 1
            else:
                return 0

        return score
    
    # public methods:

    def play(self):
        games, moves = self._get_moves()
        ranked_moves = {}
        
        for game, move in zip(games, moves):
            score = self._evaluate_state(game)
            ranked_moves.update({move: score})

        best_move = max(ranked_moves.items(), key=lambda x: x[1])[0]

        self.game.play(*best_move)

if __name__ == "__main__":
    game = Game()
    solver = AIPlayer(game, Team.crosses)

    # game loop:

    txt = ""
    while txt != 'q':
        txt = input(">")
        x, y = txt.replace(" ", "").replace(",", "")
        x = int(x)
        y = int(y)
        try:
            game.play(x, y)
            solver.play()
            print(game.state)
        except RuntimeError as e:
            print(e)
