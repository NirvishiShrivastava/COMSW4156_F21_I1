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

    if game.remaining_moves == 0:
        return jsonify(move=game.board, invalid=True, reason="No more moves remaining!", winner=game.game_result)
    if game.current_turn != 'p1':
        return jsonify(move=game.board, invalid=True, reason="Not your turn", winner=game.game_result)

    else:
        for row_num in range(5, -1, -1):
            if game.board[row_num][col_num - 1] == 0:
                game.board[row_num][col_num - 1] = game.player1
                break
            else:
                row_num -= 1

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
    if game.remaining_moves == 0:
        return jsonify(move=game.board, invalid=True, reason="No more moves remaining!", winner=game.game_result)

    if game.current_turn != 'p2':
        return jsonify(move=game.board, invalid=True, reason="Not your turn", winner=game.game_result)

    else:
        for row_num in range(5, -1, -1):
            if game.board[row_num][col_num - 1] == 0:
                game.board[row_num][col_num - 1] = game.player2
                break
            else:
                row_num -= 1

    game.current_turn = 'p1'
    game.remaining_moves -= 1

    return jsonify(move=game.board, invalid=False, winner=game.game_result)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
