from flask import Flask, request, redirect, url_for, jsonify, abort

app = Flask(__name__)

# Exercise 1: Redirect to Homepage
@app.route('/redirect-me')
def redirect_me():
    return redirect(url_for('home'))

# Exercise 2: Conditional Redirection
@app.route('/process')
def process_choice():
    choice = request.args.get('choice')
    if choice == 'dashboard':
        return redirect(url_for('dashboard'))
    elif choice == 'profile':
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    return 'Welcome to your dashboard!'

@app.route('/profile')
def profile():
    return 'This is your profile page.'

@app.route('/')
def home():
    return 'Welcome to the homepage!'

# RESTful API Routes
books = [
    {'id': 1, 'title': 'The Pragmatic Programmer', 'author': 'Andrew Hunt'},
    {'id': 2, 'title': 'Clean Code', 'author': 'Robert C. Martin'},
    {'id': 3, 'title': 'Introduction to Algorithms', 'author': 'Thomas H. Cormen'}
]

@app.route('/api/books', methods=['GET'])
def get_books():
    title = request.args.get('title')
    author = request.args.get('author')
    filtered_books = books
    if title:
        filtered_books = [book for book in filtered_books if title.lower() in book['title'].lower()]
    if author:
        filtered_books = [book for book in filtered_books if author.lower() in book['author'].lower()]
    return jsonify({'books': filtered_books})

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        abort(404)
    return jsonify({'book': book})

@app.route('/api/books', methods=['POST'])
def create_book():
    if not request.json or not 'title' in request.json or not 'author' in request.json:
        abort(400)
    new_book = {
        'id': books[-1]['id'] + 1 if books else 1,
        'title': request.json['title'],
        'author': request.json['author']
    }
    books.append(new_book)
    return jsonify({'book': new_book}), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        abort(404)
    if not request.json:
        abort(400)
    book['title'] = request.json.get('title', book['title'])
    book['author'] = request.json.get('author', book['author'])
    return jsonify({'book': book})

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        abort(404)
    books.remove(book)
    return '', 204

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

if __name__ == '__main__':
    app.run(debug=True)
