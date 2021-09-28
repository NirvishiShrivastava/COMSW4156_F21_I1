from unittest import TestCase
from Gameboard import Gameboard


class Test_TestGameboard(TestCase):

    # Test case for column fill error
    def test_col_fill_err(self):
        game = Gameboard()
        self.assertEqual(game.col_fill_err(-1), (True, "This column is already filled"))
        self.assertEqual(game.col_fill_err(0), (False, ""))

    # No game begin
    def test_check_both_players(self):
        game = Gameboard()

        game.player2 = ""
        self.assertTrue(game.check_both_players())
        game.player2 = "Yellow"
        self.assertFalse(game.check_both_players())

    # Test Draw
    def test_check_draw(self):
        game = Gameboard()
        game.remaining_moves = 0
        self.assertTrue(game.check_draw())
        game.remaining_moves = 4
        self.assertFalse(game.check_draw())

    # Test extra moves after win
    def test_check_winner(self):
        game = Gameboard()
        game.game_result = "Player1"
        self.assertTrue(game.check_winner())
        game.game_result = ""
        self.assertFalse(game.check_winner())

    # Test correct turns
    def test_check_turn(self):
        game = Gameboard()
        game.current_turn = 'p1'
        self.assertTrue(game.check_turn('p2'))
        game.current_turn = 'p2'
        self.assertFalse(game.check_turn('p2'))

    # Test to check if correct row is getting filled or not
    def test_fill_row(self):
        game = Gameboard()

        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['red', 'red', 'red', 0, 0, 0, 0]]

        self.assertEqual(game.fill_row('red', 0), 1)
        self.assertEqual(game.fill_row('red', 0), 0)

    # Test horizontal win logic
    def test_win_logic_h(self):
        game = Gameboard()

        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['red', 'red', 'red', 'red', 0, 0, 0]]
        self.assertTrue(game.win_logic_h(5, 'red'))
        self.assertFalse(game.win_logic_h(5, 'yellow'))

    # Test vertical win logic
    def test_win_logic_v(self):
        game = Gameboard()

        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['yellow', 0, 0, 0, 0, 0, 0],
                      ['yellow', 'red', 'red', 'red', 0, 0, 0]]
        self.assertTrue(game.win_logic_v(0, 'yellow'))
        self.assertFalse(game.win_logic_v(0, 'red'))

    # Test positive and negative slope diagonal win logic
    def test_win_logic_d(self):
        game = Gameboard()

        # Negative slope
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      ['red', 0, 0, 0, 0, 0, 0],
                      ['yellow', 'red', 'yellow', 0, 0, 0, 0],
                      ['yellow', 'yellow', 'red', 0, 0, 0, 0],
                      ['red', 'red', 'yellow', 'red', 0, 0, 0]]
        self.assertTrue(game.win_logic_d(2, 0, "red"))
        self.assertFalse(game.win_logic_d(3, 2, "yellow"))

        self.assertTrue(game.win_logic_d(5, 3, "red"))
        self.assertFalse(game.win_logic_d(5, 2, "yellow"))

        # Positive slope
        game.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 'red', 0, 0, 0],
                      [0, 0, 'red', 'yellow', 0, 0, 0],
                      [0, 'red', 'red', 'yellow', 0, 0, 0],
                      ['red', 'yellow', 'yellow', 'yellow', 'red', 0, 0]]
        self.assertTrue(game.win_logic_d(2, 3, 'red'))
        self.assertFalse(game.win_logic_d(3, 3, 'yellow'))

        self.assertTrue(game.win_logic_d(5, 0, "red"))
        self.assertFalse(game.win_logic_d(5, 1, "yellow"))