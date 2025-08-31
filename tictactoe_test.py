from tictactoe import Game, Team
import unittest


class TestGame(unittest.TestCase):

    # functionality:    

    def test_invalid_input(self):
        game = Game()

        with self.assertRaises(RuntimeError):
            game.play('a', 0)

    def test_overwrite(self):
        game = Game(state=[
            [' ', ' ', ' '],
            [' ', 'o', ' '],
            [' ', ' ', ' ']
        ])
        with self.assertRaises(RuntimeError):
            game.play(1, 1)

    def test_valid(self):
        with self.assertRaises(RuntimeError):
            Game(state=[
                [' ', ' ', ' '],
                [' ', 'x', ' '],
                [' ', ' ', ' ']
            ])
        with self.assertRaises(RuntimeError):
            Game(state=[
                [' ', ' ', 'x'],
                [' ', 'o', 'x'],
                [' ', ' ', ' ']
            ])

    def test_out_of_bounds(self):
        game = Game()

        with self.assertRaises(RuntimeError):
            game.play(-1, 0)
        with self.assertRaises(RuntimeError):
            game.play(0, -1)
        with self.assertRaises(RuntimeError):
            game.play(0, 3)
        with self.assertRaises(RuntimeError):
            game.play(3, 0)

    def test_no_winner(self):
        game = Game(state=[
            ['o', ' ', ' '],
            ['x', ' ', 'x'],
            [' ', ' ', 'o']
        ])
        self.assertTrue(game.winner == None)

    def test_validation(self):
        game = Game(state=[
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ])
        self.assertTrue(game.moves == 0)

        game = Game(state=[
            [' ', ' ', ' '],
            [' ', 'o', ' '],
            [' ', ' ', ' ']
        ])
        self.assertTrue(game.moves == 1)

        with self.assertRaises(RuntimeError):
            game = Game(state=[
                [' ', ' ', ' '],
                [' ', 'x', ' '],
                [' ', ' ', ' ']
            ])


    # final states:

    def test_row(self):
        game = Game(state=[
            ['o', 'o', 'o'],
            ['x', 'x', ' '],
            ['x', ' ', ' ']
        ])
        self.assertTrue(game.winner == Team.noughts)

        game = Game(state=[
            ['o', 'o', ' '],
            ['x', 'x', 'x'],
            ['o', ' ', ' ']
        ])
        self.assertTrue(game.winner == Team.crosses)

    def test_col(self):
        game = Game(state=[
            ['o', 'x', ' '],
            ['o', 'x', 'x'],
            ['o', ' ', ' ']
        ])
        self.assertTrue(game.winner == Team.noughts)

        game = Game(state=[
            ['o', 'x', ' '],
            [' ', 'x', 'o'],
            ['o', 'x', ' ']
        ])
        self.assertTrue(game.winner == Team.crosses)

    def test_diag(self):
        game = Game(state=[
            ['o', 'x', ' '],
            ['x', 'o', 'x'],
            [' ', ' ', 'o']
        ])
        self.assertTrue(game.winner == Team.noughts)

        game = Game(state=[
            ['o', ' ', 'x'],
            [' ', 'x', 'o'],
            ['x', ' ', 'o']
        ])
        self.assertTrue(game.winner == Team.crosses)

        


if __name__ == "__main__":
    unittest.main()