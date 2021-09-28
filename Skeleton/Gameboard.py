

import db

class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42

    def check_both_players(self):
        return self.player2 == ""

    def check_draw(self):
        return self.remaining_moves == 0

    def check_winner(self):
        return len(self.game_result) > 0

    def check_turn(self,turn_p):
        return self.current_turn != turn_p

    def fill_row(self, player, col_num):
        for row_num in range(5, -1, -1):
            if self.board[row_num][col_num] == 0:
                self.board[row_num][col_num] = player
                break
            else:
                row_num -= 1

        return row_num

    def col_fill_err(self, row_num):
        invalid = False
        reason = ""

        if row_num < 0:
            invalid = True
            reason = "This column is already filled"

        return invalid, reason

    def win_logic_h(self, row_num, player):
        """
        Horizontal Win
        """

        counter = 0
        for c in range(0, 7):
            if self.board[row_num][c] == player:
                counter += 1
                if counter == 4:
                    return True
            else:
                counter = 0
        return False

    def win_logic_v(self, col_num, player):
        """
        Vertical Win
        """
        counter = 0
        for r in range(0, 6):
            if self.board[r][col_num] == player:
                counter += 1
                if counter == 4:
                    return True
            else:
                counter = 0
        return False

    def win_logic_d(self, r, c, player):
        """
        Diagonal Win
        """
        counter = 0
        for i in range(4):
            if r - i <= 5 and c - i <= 6 and self.board[r - i][c - i] == player:
                counter += 1
                if counter == 4:
                    return True
            else:
                counter = 0

        counter = 0
        for i in range(4):
            if r + i <= 5 and c + i <= 6 and self.board[r + i][c + i] == player:
                counter += 1
                if counter == 4:
                    return True
            else:
                counter = 0

        counter = 0
        for i in range(4):
            if r - i <= 5 and c + i <= 6 and self.board[r - i][c + i] == player:
                counter += 1
                if counter == 4:
                    return True
            else:
                counter = 0

        counter = 0
        for i in range(4):
            if r + i <= 5 and c - i <= 6 and self.board[r + i][c - i] == player:
                counter += 1
                if counter == 4:
                    return True
            else:
                counter = 0
        return False



    
