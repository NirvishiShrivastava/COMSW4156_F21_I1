

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

    def check_turn(self, turn_p):
        return self.current_turn != turn_p

    def err_check(self, turn):

        invalid = False
        reason = ""

        if self.check_both_players():
            invalid = True
            reason = "Game cannot begin till both players join"

        elif self.check_draw():
            invalid = True
            reason = "Match Draw!"

        elif self.check_winner():
            invalid = True
            reason = "No moves allowed if there is a winner"

        elif self.check_turn(turn):
            invalid = True
            reason = "Not your turn"

        return invalid, reason

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
            if r - i <= 5 and c - i <= 6 and self.board[
               r - i][c - i] == player:
                counter += 1
                if counter == 4:
                    return True
            else:
                counter = 0

        counter = 0
        for i in range(4):
            if r + i <= 5 and c + i <= 6 and self.board[
               r + i][c + i] == player:
                counter += 1
                if counter == 4:
                    return True
            else:
                counter = 0

        counter = 0
        for i in range(4):
            if r - i <= 5 and c + i <= 6 and self.board[
                    r - i][c + i] == player:
                counter += 1
                if counter == 4:
                    return True
            else:
                counter = 0

        counter = 0
        for i in range(4):
            if r + i <= 5 and c - i <= 6 and self.board[
               r + i][c - i] == player:
                counter += 1
                if counter == 4:
                    return True
            else:
                counter = 0
        return False

    def player_move(self, col_num, turn, color):

        winner = self.game_result

        invalid, reason = self.err_check(turn)

        if not invalid:
            row_num = self.fill_row(color, col_num)

            invalid, reason = self.col_fill_err(row_num)

            if self.win_logic_h(row_num, color) or self.win_logic_v(
               col_num, color) or self.win_logic_d(
                    row_num, col_num, color):
                self.game_result = "Player "+turn[-1]
                winner = self.game_result

            self.current_turn = 'p2' if turn == 'p1' else 'p1'
            self.remaining_moves -= 1

            # Add details to the database
            move_db = (self.current_turn, str(self.board), winner, self.player1, self.player2, self.remaining_moves)
            db.add_move(move_db)

        return invalid, reason, winner
