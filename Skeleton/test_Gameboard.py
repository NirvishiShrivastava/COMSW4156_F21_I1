from unittest import TestCase
from Gameboard import Gameboard


class Test_TestGameboard(TestCase):

    def setUp(self):
        self.game = Gameboard()

    def tearDown(self):
        del self.game

    # Test case for column fill error
    def test_col_fill_err(self):
        self.assertEqual(self.game.col_fill_err(-1), (True,
                         "This column is already filled"))
        self.assertEqual(self.game.col_fill_err(0), (False, ""))

    # No game begin
    def test_check_both_players(self):
        self.game.player2 = ""
        self.assertTrue(self.game.check_both_players())
        self.game.player2 = "Yellow"
        self.assertFalse(self.game.check_both_players())

    # Test Draw
    def test_check_draw(self):
        self.game.remaining_moves = 0
        self.assertTrue(self.game.check_draw())
        self.game.remaining_moves = 4
        self.assertFalse(self.game.check_draw())

    # Test extra moves after win
    def test_check_winner(self):
        self.game.game_result = "Player1"
        self.assertTrue(self.game.check_winner())
        self.game.game_result = ""
        self.assertFalse(self.game.check_winner())

    # Test correct turns
    def test_check_turn(self):
        self.game.current_turn = 'p1'
        self.assertTrue(self.game.check_turn('p2'))
        self.game.current_turn = 'p2'
        self.assertFalse(self.game.check_turn('p2'))

    # Test to check if correct row is getting filled or not
    def test_fill_row(self):
        self.game.board = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           ['yellow', 0, 0, 0, 0, 0, 0],
                           ['yellow', 0, 0, 0, 0, 0, 0],
                           ['yellow', 0, 0, 0, 0, 0, 0],
                           ['red', 'red', 'red', 0, 0, 0, 0]]

        self.assertEqual(self.game.fill_row('red', 0), 1)
        self.assertEqual(self.game.fill_row('red', 0), 0)

    # Test horizontal win logic
    def test_win_logic_h(self):
        self.game.board = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           ['yellow', 0, 0, 0, 0, 0, 0],
                           ['yellow', 0, 0, 0, 0, 0, 0],
                           ['yellow', 0, 0, 0, 0, 0, 0],
                           ['red', 'red', 'red', 'red', 0, 0, 0]]
        self.assertTrue(self.game.win_logic_h(5, 'red'))
        self.assertFalse(self.game.win_logic_h(5, 'yellow'))

    # Test vertical win logic
    def test_win_logic_v(self):
        self.game.player1 = 'yellow'
        self.game.player2 = 'red'
        self.game.board = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           ['yellow', 0, 0, 0, 0, 0, 0],
                           ['yellow', 0, 0, 0, 0, 0, 0],
                           ['yellow', 'red', 'red', 'red', 0, 0, 0]]

        self.game.current_turn = 'p1'
        invalid, _, winner = self.game.player_move(0, 'p1', self.game.player1)
        self.assertEqual((invalid, winner), (False, 'Player 1'))

    # Test positive and negative slope diagonal win logic
    def test_win_logic_d(self):
        # Negative slope
        self.game.board = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           ['red', 0, 0, 0, 0, 0, 0],
                           ['yellow', 'red', 'yellow', 0, 0, 0, 0],
                           ['yellow', 'yellow', 'red', 0, 0, 0, 0],
                           ['red', 'red', 'yellow', 'red', 0, 0, 0]]
        self.assertTrue(self.game.win_logic_d(2, 0, "red"))
        self.assertFalse(self.game.win_logic_d(3, 2, "yellow"))

        self.assertTrue(self.game.win_logic_d(5, 3, "red"))
        self.assertFalse(self.game.win_logic_d(5, 2, "yellow"))

        # Positive slope
        self.game.board = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 'red', 0, 0, 0],
                           [0, 0, 'red', 'yellow', 0, 0, 0],
                           [0, 'red', 'red', 'yellow', 0, 0, 0],
                           ['red', 'yellow', 'yellow', 'yellow', 'red', 0, 0]]
        self.assertTrue(self.game.win_logic_d(2, 3, 'red'))
        self.assertFalse(self.game.win_logic_d(3, 3, 'yellow'))

        self.assertTrue(self.game.win_logic_d(5, 0, "red"))
        self.assertFalse(self.game.win_logic_d(5, 1, "yellow"))

    # Happy Path function
    def test_happy_path(self):
        self.game.player1 = "red"
        self.game.player2 = "yellow"
        self.game.board = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           ['red', 'yellow', 0, 0, 0, 0, 0]]
        self.game.current_turn = 'p1'

        self.assertEqual(self.game.player_move(0, 'p1',
                         self.game.player1)[0], False)
        self.assertEqual(self.game.player_move(0, 'p1',
                         self.game.player1)[0], True)

        self.assertEqual(self.game.board[4][0], 'red')

    # Test to check if invalid player is not connected
    def test_invalid_player_not_connected(self):
        self.assertEqual(self.game.player_move(0, 'p1',
                         self.game.player1)[0], True)
        self.assertEqual(self.game.player_move(0, 'p2',
                         self.game.player1)[0], True)

    # Test to check invalid move after draw
    def test_invalid_move_after_draw(self):
        self.game.player1 = 'red'
        self.game.player2 = 'yellow'
        self.game.remaining_moves = 0

        self.assertEqual(self.game.player_move(0, 'p1',
                         self.game.player1)[0], True)

    # Test to check player move after win
    def test_check_win(self):
        self.game.player1 = 'red'
        self.game.player2 = 'yellow'
        self.game.game_result = 'Player 1'

        self.assertEqual(self.game.player_move(0, 'p1',
                         self.game.player1)[0], True)
