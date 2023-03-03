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

def add_book(conn, cur, book_data):
    """ Add a book to the database """
    sql = """INSERT INTO books VALUES(%s, %s, %s, %s);"""
    cur.execute(
        sql, (
            book_data['isbn'], book_data['title'],
            book_data['read'], book_data['rating'],
            )
        )
    conn.commit()

def add_author():
    """ Add an author to the database """
    sql = """INSERT INTO authors(name) VALUES(%s);"""

def add_book_author():
    """  """
    
