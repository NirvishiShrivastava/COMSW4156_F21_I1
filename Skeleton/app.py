from flask import Flask, render_template, request, redirect, jsonify
from Gameboard import Gameboard
import db
import logging
import ast


app = Flask(__name__)


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = Gameboard()

'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():
    db.clear()
    db.init_db()
    global game
    game = Gameboard()
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

    state = db.getMove()

    if state is None or len(state) == 0:
        p1color_picked = request.args.get('color')
        game.player1 = p1color_picked
    else:
        game.current_turn = state[0]
        board_str = ast.literal_eval(state[1])
        game.board = board_str
        game.game_result = state[2]
        game.player1 = state[3]
        game.player2 = state[4]
        game.remaining_moves = state[5]
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
    state = db.getMove()
    if state is None or len(state) == 0:
        if game.player1 == 'red':
            game.player2 = 'yellow'
        elif game.player1 == 'yellow':
            game.player2 = 'red'
        else:
            game.player2 = "Error - Player 1 has not selected a color"
    else:
        game.current_turn = state[0]
        board_str = ast.literal_eval(state[1])
        game.board = board_str
        game.game_result = state[2]
        game.player1 = state[3]
        game.player2 = state[4]
        game.remaining_moves = state[5]
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
    col_num -= 1

    invalid, reason, winner = game.player_move(
        col_num, 'p1', game.player1)
    return jsonify(move=game.board, invalid=invalid,
                   reason=reason, winner=winner)


'''
Same as '/move1' but instead process Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    post_det = request.get_json()
    col_num = int((post_det['column'])[-1])
    col_num -= 1

    invalid, reason, winner = game.player_move(col_num, 'p2', game.player2)

    return jsonify(move=game.board,
                   invalid=invalid, reason=reason, winner=winner)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
