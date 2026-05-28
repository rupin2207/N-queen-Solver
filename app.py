from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

def is_safe(board, row, col, n):
    for i in range(row):
        if board[i][col] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, n)):
        if board[i][j] == 1:
            return False
    return True

def solve_n_queens(board, row, n):
    if row >= n:
        return True
    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = 1
            if solve_n_queens(board, row + 1, n):
                return True
            board[row][col] = 0
    return False

def get_solution(n):
    board = [[0 for _ in range(n)] for _ in range(n)]
    if solve_n_queens(board, 0, n):
        return board
    else:
        return None

def validate_board(board):
    n = len(board)
    if n == 0:
        return False
    # Check rows
    for row in board:
        if row.count(1) > 1:
            return False
    # Check columns
    for col in range(n):
        count = sum(board[row][col] for row in range(n))
        if count > 1:
            return False
    # Check diagonals
    for i in range(-n + 1, n):
        if sum(board[row][row + i] for row in range(n) if 0 <= row + i < n) > 1:
            return False
        if sum(board[row][n - row - 1 - i] for row in range(n) if 0 <= n - row - 1 - i < n) > 1:
            return False
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    solution = None
    n = None
    if request.method == 'POST':
        n = int(request.form['n-value'])
        mode = request.form['mode']
        if mode == 'computer':
            solution = get_solution(n)
    return render_template('index.html', solution=solution, n=n)

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    board = data['board']
    valid = validate_board(board)
    return jsonify({'valid': valid})

@app.route('/hint', methods=['POST'])
def hint():
    data = request.get_json()
    n = data['n-value']
    solution = get_solution(n)
    return jsonify({'solution': solution})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
