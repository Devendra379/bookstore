from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors

app = Flask(__name__)

# Database configuration
db_host = 'mybookstore.c1asikkcok9v.ap-southeast-2.rds.amazonaws.com'
db_user = 'myadmin'
db_password = 'mybookstore'
db_name = 'mybookstore'

# Function to connect to the database
def connect_to_database():
    return pymysql.connect(host=db_host,
                           user=db_user,
                           password=db_password,
                           database=db_name,
                           cursorclass=pymysql.cursors.DictCursor)

# Route to display books
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        try:
            connection = connect_to_database()
            with connection.cursor() as cursor:
                # Search for books by title, author, or ISBN
                cursor.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s", 
                               ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
                books = cursor.fetchall()
            connection.close()
            return render_template('index.html', books=books, search_query=search_query)
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        try:
            connection = connect_to_database()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM books")
                books = cursor.fetchall()
            connection.close()
            return render_template('index.html', books=books, search_query='')
        except Exception as e:
            return f"An error occurred: {e}"

# Route to add a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        price = request.form['price']
        try:
            connection = connect_to_database()
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO books (title, author, isbn, price) VALUES (%s, %s, %s, %s)", (title, author, isbn, price))
                connection.commit()
            connection.close()
            return redirect(url_for('index'))
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template('add_book.html')

# Route to delete a book
@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    try:
        connection = connect_to_database()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
            connection.commit()
        connection.close()
        return redirect(url_for('index'))
    except Exception as e:
        return f"An error occurred: {e}"

# Route to update a book
@app.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        price = request.form['price']
        try:
            connection = connect_to_database()
            with connection.cursor() as cursor:
                cursor.execute("UPDATE books SET title=%s, author=%s, isbn=%s, price=%s WHERE id=%s", (title, author, isbn, price, book_id))
                connection.commit()
            connection.close()
            return redirect(url_for('index'))
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        try:
            connection = connect_to_database()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
                book = cursor.fetchone()
            connection.close()
            return render_template('update_book.html', book=book)
        except Exception as e:
            return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
