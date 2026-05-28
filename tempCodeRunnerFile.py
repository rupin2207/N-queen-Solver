@app.route('/', methods=['GET', 'POST'])
def index():
    solution = None
    if request.method == 'POST':
        n = int(request.form['n-value'])
        print(f"Received input: {n}")  # Debug print
        solution = get_solution(n)
        print(f"Generated solution: {solution}")  # Debug print
    return render_template('index.html', solution=solution)
@app.route('/solve', methods=['POST'])
def solve():
    n = int(request.form['n-value'])
    solution = get_solution(n)
    return render_template('index.html', solution=solution)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)