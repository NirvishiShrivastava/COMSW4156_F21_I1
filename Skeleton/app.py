from flask import Flask, render_template, request, redirect, jsonify
from json import dump
from Gameboard import Gameboard
import db

app = Flask(__name__)

import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

global game
game = Gameboard()

'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():
    return render_template("player1_connect.html", status="Pick a Color.")


'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")


'''
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
'''


@app.route('/p1Color', methods=['GET'])
def player1_config():
    p1color_picked = request.args.get('color')
    game.player1 = p1color_picked
    return render_template("player1_connect.html", status=game.player1)


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():
    if game.player1 == 'red':
        game.player2 = 'yellow'
    elif game.player1 == 'yellow':
        game.player2 = 'red'
    else:
        game.player2 = "Error - Player 1 has not selected a color"
    return render_template("p2Join.html", status=game.player2)


'''
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move
'''


@app.route('/move1', methods=['POST'])
def p1_move():
    post_det = request.get_json()
    col_num = int((post_det['column'])[-1])
    if game.remaining_moves == 1:
        return jsonify(move=game.board, invalid=True, reason="Match Draw!", winner=game.game_result)

    if game.current_turn != 'p1':
        return jsonify(move=game.board, invalid=True, reason="Not your turn", winner=game.game_result)

    else:
        row_num = fill_row(game.player1, col_num)

        if win_logic(row_num, col_num, game.player1):
            game.game_result = "Player1"
            return jsonify(move=game.board, invalid=False, winner=game.game_result)

    game.current_turn = 'p2'
    game.remaining_moves -= 1

    return jsonify(move=game.board, invalid=False, winner=game.game_result)


'''
Same as '/move1' but instead process Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    post_det = request.get_json()
    col_num = int((post_det['column'])[-1])
    if game.remaining_moves == 1:
        return jsonify(move=game.board, invalid=True, reason="Match Draw!", winner=game.game_result)

    if game.current_turn != 'p2':
        return jsonify(move=game.board, invalid=True, reason="Not your turn", winner=game.game_result)

    else:
        row_num = fill_row(game.player2, col_num)

        if win_logic(row_num, col_num, game.player2):
            game.game_result = "Player2"
            return jsonify(move=game.board, invalid=False, winner=game.game_result)

    game.current_turn = 'p1'
    game.remaining_moves -= 1

    return jsonify(move=game.board, invalid=False, winner=game.game_result)


def fill_row(player, col_num):
    for row_num in range(5, -1, -1):
        if game.board[row_num][col_num - 1] == 0:
            game.board[row_num][col_num - 1] = player
            break
        else:
            row_num -= 1
            if row_num == -1:
                return jsonify(move=game.board, invalid=True, reason="This column is already filled",
                               winner=game.game_result)
    return row_num


def win_logic(row_num, col_num, player):
    """
    Horizontal Win
    """
    print("Win logic called for row, col" + str(row_num) + "," + str(col_num))
    counter1 = 0
    for c in range(0, 7):
        if game.board[row_num][c] == player:
            counter1 += 1
            print("Counter for row and col -- ", counter1, row_num, c)
    if counter1 == 4:
        return True
    else:
        return False

    """
    Vertical Win
    """
    counter2 = 0
    for r in range(0, 6):
        if game.board[r][col_num] == player:
            counter2 += 1
            print("Counter for row and col -- ", counter2, r, col_num)
    if counter2 == 4:
        return True
    else:
        return False

    """
    Diagonal Win
    """
    counter3 = 0
    for r in range(0, 6):
        for c in range(0, 7):
            if game.board[r][c] == player:
                counter3 += 1
    if counter3 == 4:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
