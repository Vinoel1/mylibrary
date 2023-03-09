import psycopg2
from config import config

def db_connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    cur = None
    try:
        # Read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the database...')
        conn = psycopg2.connect(**params)
		
        # Create a cursor
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    return conn, cur

def db_close(conn, cur):
    """ Close communication with the database """
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
        print('Database connection closed.')

def check_book_in_db(conn, cur, isbn):
    """ Check if the ISBN given by the user matches a book that is already
    in the database """
    sql = """SELECT * FROM books WHERE isbn = %s;"""
    try:
        cur.execute(sql, (isbn,))
        row = cur.fetchone()

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

def add_book(conn, cur, book_data):
    """ Add a book to the database """
    sql = """INSERT INTO books VALUES(%s, %s, %s, %s);"""
    try:
        cur.execute(
            sql, (
                book_data['isbn'], book_data['title'],
                book_data['read'], book_data['rating']
                )
            )
        conn.commit()
        return 1
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("The book could not be added to the database")
        return 0

def add_author():
    """ Add an author to the database """
    sql = """INSERT INTO authors(name) VALUES(%s);"""
    # TODO

def add_book_author():
    """  """
    # TODO
    
def modify_book_info():
    """  """
    # TODO
