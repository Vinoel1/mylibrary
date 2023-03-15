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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    return conn

def db_close(conn):
    """ Close communication with the database """
    if conn is not None:
        conn.close()
        print('Database connection closed.')

def check_book_in_db(conn, isbn):
    """ Check if the ISBN given by the user matches a book that is already
    in the database """
    sql = """SELECT * FROM books WHERE isbn = %s;"""
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cur.execute(sql, (isbn,))
        row = cur.fetchone()
        cur.close()

        # The book is already in the database, print and return the row
        if row is not None:
            print(f"Book with ISBN {isbn} is already present in the database")
            print("About this book:")
            print(row)
            return row
        # The book is not in the database
        else:
            return None
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

def add_book(conn, book_data):
    """ Add a book to the database """
    sql = """INSERT INTO books VALUES(%s, %s, %s, %s);"""
    try:
        cur = conn.cursor()
        cur.execute(
            sql, (
                book_data['isbn'], book_data['title'],
                book_data['read'], book_data['rating']
                )
            )
        conn.commit()
        cur.close()
        
        # Print collected information
        print("The following information has been added to the database:")
        print(book_data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("The book could not be added to the database")

def add_author(conn, authors):
    """ Add an author to the database """
    sql = """INSERT INTO authors(name) VALUES(%s);"""
    try:
        cur = conn.cursor()
        cur.execute(sql, (authors,))
        conn.commit()
        cur.close()
        
        # Print collected information
        print(f"{authors} has been added to the database")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print(f"{authors} could not be added to the database")

def add_book_author():
    """  """
    # TODO
    
def modify_book_info(conn, book_data):
    """ Modify user information on a book (read status and rating) """
    sql = """UPDATE books SET read = %s, rating = %s WHERE isbn = %s;"""
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
        print("The following information has been added to the database:")
        print(book_data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("The information about this book could not be modified")

def delete_book_info(conn, isbn):
    """ Delete a book from the database """
    sql = """DELETE FROM books WHERE isbn = %s;"""
    try:
        cur = conn.cursor()
        cur.execute(sql, (isbn,))
        conn.commit()
        cur.close()
        
        print("The book has been successfully deleted")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("The book could not be deleted")
