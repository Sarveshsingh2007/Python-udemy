from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

def check_winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != '' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_draw(board):
    return all(cell != '' for cell in board) and check_winner(board) is None

def move_easy(board):
    empty = [i for i, v in enumerate(board) if v == '']
    return random.choice(empty) if empty else None

def move_standard(board, comp='O', human='X'):
    for i in range(9):
        if board[i] == '':
            board[i] = comp
            if check_winner(board) == comp:
                board[i] = ''
                return i
            board[i] = ''
    for i in range(9):
        if board[i] == '':
            board[i] = human
            if check_winner(board) == human:
                board[i] = ''
                return i
            board[i] = ''
    return move_easy(board)

def minimax(board, player, comp='O', human='X'):
    winner = check_winner(board)
    if winner == comp:
        return {'score': 1}
    elif winner == human:
        return {'score': -1}
    elif is_draw(board):
        return {'score': 0}

    moves = []
    for i in range(9):
        if board[i] == '':
            board[i] = player
            result = minimax(board, comp if player == human else human, comp, human)
            moves.append({'index': i, 'score': result['score']})
            board[i] = ''
    if player == comp:
        return max(moves, key=lambda x: x['score'])
    else:
        return min(moves, key=lambda x: x['score'])

def move_intermediate(board, comp='O', human='X'):
    if all(cell == '' for cell in board):
        return 4 if board[4] == '' else 0
    return minimax(board, comp, comp, human)['index']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/computer_move', methods=['POST'])
def computer_move():
    data = request.get_json()
    board = data.get('board', [])
    difficulty = data.get('difficulty', 'easy')
    comp = data.get('computer', 'O')
    human = 'X' if comp == 'O' else 'O'

    if difficulty == 'easy':
        idx = move_easy(board)
    elif difficulty == 'standard':
        idx = move_standard(board, comp, human)
    else:
        idx = move_intermediate(board, comp, human)

    if idx is None:
        return jsonify({'move': None, 'board': board, 'winner': None, 'draw': is_draw(board)})

    board[idx] = comp
    return jsonify({
        'move': idx,
        'board': board,
        'winner': check_winner(board),
        'draw': is_draw(board)
    })

if __name__ == '__main__':
    app.run(debug=True)
