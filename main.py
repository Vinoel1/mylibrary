""" Fill your personal digital library using Google Books API
and a PostgreSQL database """

import json
from urllib.request import urlopen
import book_info
import manage_database

# Connect to the database
conn = manage_database.db_connect()

if conn is not None:
    while True:
        # Send a request to the Google Books API
        api = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'
        isbn = input('Enter a 10 or 13 digit ISBN: ').strip()
        # Test ISBN
        # isbn = '9782075062824'
        book_data = manage_database.check_book_in_db(conn, isbn)

        if book_data is not None and book_data != 0:
            # Ask user if they would like to modify their info about this book
            while True:
                modify_book = input(
                    'Would you like to modify the information you gave on '
                    'this book? yes or no '
                    ).lower().strip()

                # Stop asking when the answer is 'yes' or 'no'
                if modify_book in {'yes', 'no'}:
                    break

            if modify_book == 'yes':
                # Ask user if they have read the book
                # If they have, then ask for a rating and store in book_data
                book_data = book_info.ask_if_read_and_rate(book_data)
                # Modify information in the database
                manage_database.modify_book_info(conn, book_data)
            else:
                # Ask user if they would like to delete this book
                while True:
                    delete_book = input(
                        'Would you like to delete this book from the '
                        'database? yes or no '
                        ).lower().strip()

                    # Stop asking when the answer is 'yes' or 'no'
                    if delete_book in {'yes', 'no'}:
                        break

                # Delete book from the database
                if delete_book == 'yes':
                    deleted = manage_database.delete_all_book_info(conn, isbn)
                    if deleted is True:
                        print('The book has been successfully deleted from '
                              'the database')

        elif book_data is None:
            with urlopen(api + isbn) as response:
                # Store JSON response in a dictionary
                data_raw = json.load(response)

            # Store title and authors information in book_data dictionnary
            book_data, authors = book_info.parse_raw(isbn, data_raw)
            # Ask user if they have read the book
            # If they have, then ask for a rating and store in book_data
            book_data = book_info.ask_if_read_and_rate(book_data)

            # Add book and authors to the database
            added = manage_database.add_all_book_info(
                conn, book_data, authors
                )
            if added is True:
                # Print collected information
                print(
                    'The following information has been added to the '
                    'database:'
                    )
                print(book_data)
        else:
            print('Could not check if the book is in the database')

        # Ask user if they would like to add another book
        while True:
            user_update = input(
                'Would you like to enter another ISBN? yes or no '
                ).lower().strip()

            # Stop asking when the answer is 'yes' or 'no'
            if user_update in {'yes', 'no'}:
                break

        # Break out of the loop
        if user_update == 'no':
            break
else:
    print('Could not connect to the database')

# Close communication with the database
manage_database.db_close(conn)
