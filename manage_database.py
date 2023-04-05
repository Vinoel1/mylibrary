""" All functions for handling the database: connection, reading, adding,
modifying and deleting information """

import psycopg2
import psycopg2.extras
from config import config


def db_connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # Read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the database...')
        conn = psycopg2.connect(**params)
    except psycopg2.Error as error:
        print(error)

    return conn


def db_close(conn):
    """ Close communication with the database """
    if conn is not None:
        conn.close()
        print('Database connection closed')


def check_book_in_db(conn, isbn):
    """ Check if the ISBN given by the user matches a book that is already
    in the database """
    sql = "SELECT * FROM books WHERE isbn = %s;"
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cur.execute(sql, (isbn,))
        row = cur.fetchone()
        cur.close()

        # The book is already in the database, print and return the row
        if row is not None:
            print(f'Book with ISBN {isbn} is already present in the database')
            print('About this book:')
            print(row)
            return row
        # The book is not in the database
        return None
    except psycopg2.Error as error:
        print(error)
        return 0


def check_author_in_db(conn, author):
    """ Check if the author is already in the database """
    sql = "SELECT author_id FROM authors WHERE name = %s;"
    try:
        cur = conn.cursor()
        cur.execute(sql, (author,))
        row = cur.fetchone()
        cur.close()

        # The author is already in the database
        if row is not None:
            return row
        # The author is not in the database
        return 0
    except psycopg2.Error as error:
        print(error)
        return None


def get_author_id(conn, isbn):
    """ Return identifiers of a book's authors """
    sql = "SELECT author_id FROM book_authors WHERE isbn = %s;"
    cur = conn.cursor()
    cur.execute(sql, (isbn,))
    rows = cur.fetchall()
    cur.close()

    return rows


def check_books_written(conn, isbn, author_id):
    """ Check if the author has written another book in the database """
    sql = "SELECT isbn FROM book_authors WHERE author_id = %s AND isbn != %s;"
    cur = conn.cursor()
    cur.execute(sql, (author_id, isbn))
    rows = cur.fetchall()
    cur.close()

    # The author has written other books stored in the database
    if rows is not None:
        return True
    # The author has not written another book stored in the database
    return False


def add_book(conn, book_data):
    """ Add a book to the database """
    sql = "INSERT INTO books VALUES(%s, %s, %s, %s);"
    cur = conn.cursor()
    cur.execute(
        sql, (
            book_data['isbn'], book_data['title'],
            book_data['read'], book_data['rating']
            )
        )
    cur.close()


def add_author(conn, authors):
    """ Add an author to the database """
    sql = "INSERT INTO authors(name) VALUES(%s) RETURNING author_id;"
    cur = conn.cursor()
    cur.execute(sql, (authors,))
    author_id = cur.fetchone()[0]
    cur.close()

    return author_id


def add_book_author(conn, isbn, author_id):
    """ Add the relation between a book and its authors to the database """
    sql = "INSERT INTO book_authors VALUES(%s, %s);"
    cur = conn.cursor()
    cur.execute(sql, (isbn, author_id))
    cur.close()


def add_all_book_info(conn, book_data, authors):
    """ Add a book and its authors to the database """
    added = False
    try:
        add_book(conn, book_data)
        # Check if the authors are already in the database
        for author in authors:
            author_id = check_author_in_db(conn, author)
            # If they are not, add them
            if author_id == 0:
                author_id = add_author(conn, author)
            add_book_author(conn,  book_data['isbn'], author_id)

        conn.commit()
        added = True
    except psycopg2.Error as error:
        print(error)
        print('The book could not be added to the database')

    return added


def modify_book_info(conn, book_data):
    """ Modify user information on a book (read status and rating) """
    sql = "UPDATE books SET read = %s, rating = %s WHERE isbn = %s;"
    try:
        cur = conn.cursor()
        cur.execute(
            sql, (
                book_data['read'], book_data['rating'], book_data['isbn']
                )
            )
        conn.commit()
        cur.close()

        # Print collected information
        print('The following information has been added to the database:')
        print(book_data)
    except psycopg2.Error as error:
        print(error)
        print('The information could not be modified')


def delete_book_author(conn, isbn):
    """ Delete the relation between a book and its authors
    from the database """
    sql = "DELETE FROM book_authors WHERE isbn = %s;"
    cur = conn.cursor()
    cur.execute(sql, (isbn,))
    cur.close()


def delete_author(conn, isbn, author_id):
    """ Delete an author from the database """
    # Check if the author has written another book in the database
    other_books = check_books_written(conn, isbn, author_id)
    # If not, delete the author
    if other_books is True:
        sql = "DELETE FROM authors WHERE author_id = %s;"
        cur = conn.cursor()
        cur.execute(sql, (author_id,))
        cur.close()


def delete_book(conn, isbn):
    """ Delete a book from the database """
    sql = "DELETE FROM books WHERE isbn = %s;"
    cur = conn.cursor()
    cur.execute(sql, (isbn,))
    cur.close()


def delete_all_book_info(conn, isbn):
    """ Delete a book and its authors from the database """
    deleted = False
    try:
        delete_book_author(conn, isbn)
        author_ids = get_author_id(conn, isbn)
        for author_id in author_ids:
            delete_author(conn, isbn, author_id)
        delete_book(conn, isbn)

        conn.commit()
        deleted = True
    except psycopg2.Error as error:
        print(error)
        print('The book could not be deleted drom the database')

    return deleted
