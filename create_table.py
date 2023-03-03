import psycopg2
from config import config

def create_tables():
    """ Create tables in the PostgreSQL database """
    commands = (
        """
        CREATE TABLE books (
            isbn VARCHAR(13),
            title VARCHAR(200) NOT NULL,
            read BOOLEAN NOT NULL,
            rating INTEGER NOT NULL,
            PRIMARY KEY(isbn)
        )
        """,
        """
        CREATE TABLE authors (
            author_id SERIAL,
            name VARCHAR(200) NOT NULL,
            PRIMARY KEY(author_id)
        )
        """,
        """
        CREATE TABLE book_authors (
            isbn VARCHAR(13),
            author_id SERIAL,
            PRIMARY KEY(isbn, author_id),
            FOREIGN KEY(isbn) REFERENCES books(isbn),
            FOREIGN KEY(author_id) REFERENCES authors(author_id)
        )
        """)
    conn = None

    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
