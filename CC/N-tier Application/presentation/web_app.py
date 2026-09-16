from flask import Flask, render_template, request, redirect, url_for, flash
from business.book_manager import BookManager
from business.exceptions import BookException

class WebApp:
    def __init__(self, book_manager: BookManager):
        self.manager = book_manager
        self.app = Flask(__name__, template_folder='templates', static_folder='static')
        self.app.secret_key = 'super_secret_key_for_flash_messages'  # Needed for flash()
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/', methods=['GET'])
        def index():
            query = request.args.get('query', '').strip()
            if query:
                books = self.manager.search_books(query)
            else:
                books = self.manager.view_all_books()
            return render_template('index.html', books=books, query=query)

        @self.app.route('/add', methods=['POST'])
        def add_book():
            try:
                title = request.form.get('title')
                author = request.form.get('author')
                isbn = request.form.get('isbn')
                year = int(request.form.get('year'))
                quantity = int(request.form.get('quantity'))
                
                self.manager.add_book(title, author, isbn, year, quantity)
                flash('Book added successfully!', 'success')
            except ValueError:
                flash('Year and Quantity must be valid integers.', 'error')
            except BookException as e:
                flash(str(e), 'error')
                
            return redirect(url_for('index'))

        @self.app.route('/checkout/<int:book_id>', methods=['POST'])
        def checkout_book(book_id):
            try:
                self.manager.check_out_book(book_id)
                flash('Book checked out successfully!', 'success')
            except BookException as e:
                flash(str(e), 'error')
                
            return redirect(url_for('index'))

        @self.app.route('/update/<int:book_id>', methods=['GET', 'POST'])
        def update_book(book_id):
            try:
                book = self.manager.get_book(book_id)
            except BookException as e:
                flash(str(e), 'error')
                return redirect(url_for('index'))

            if request.method == 'POST':
                try:
                    title = request.form.get('title')
                    author = request.form.get('author')
                    isbn = request.form.get('isbn')
                    year = int(request.form.get('year'))
                    quantity = int(request.form.get('quantity'))
                    
                    self.manager.update_book(book_id, title, author, isbn, year, quantity)
                    flash('Book updated successfully!', 'success')
                    return redirect(url_for('index'))
                except ValueError:
                    flash('Year and Quantity must be valid integers.', 'error')
                except BookException as e:
                    flash(str(e), 'error')
            
            return render_template('update.html', book=book)

        @self.app.route('/delete/<int:book_id>', methods=['POST'])
        def delete_book(book_id):
            try:
                self.manager.delete_book(book_id)
                flash('Book deleted successfully!', 'success')
            except BookException as e:
                flash(str(e), 'error')
                
            return redirect(url_for('index'))

    def run(self, host='127.0.0.1', port=5000):
        # Disable debug mode in production, but okay for a simple local app
        self.app.run(host=host, port=port, debug=False)
