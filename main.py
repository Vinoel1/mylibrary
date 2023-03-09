import json
from urllib.request import urlopen
import book_info_user
import manage_database

# Connect to the database
conn, cur = manage_database.db_connect()

while True:
    # Send a request to the Google Books API
    api = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'
    isbn = input('Enter a 10 or 13 digit ISBN: ').strip()
    # Test ISBN
    # isbn = '9782075062824'
    book_data = manage_database.check_book_in_db(conn, cur, isbn)

    if book_data is not None:
        # Ask user if they would like to modify their info about this book
        while True:
            user_update = input(
                'Would you like to modify the information you gave on this '
                'book? yes or no '
                ).lower().strip()

            # Stop asking when the answer is 'yes' or 'no'
            if user_update == 'yes' or user_update == 'no':
                break
        
        # Modify read status and rating in the database
        if user_update == 'yes':
            # Add user if they have read the book and store the answer
            book_data['read'] = book_info_user.has_been_read()

            # If the book has been read, ask for a rating
            if book_data['read'] == 'true':
                book_data['rating'] = book_info_user.rate_book()
            # If the book has not been read, set rating to None
            else:
                book_data['rating'] = None
            # TODO call modify_book_info
    else:
        response = urlopen(api + isbn)
        # Store JSON response in a dictionary
        data_raw = json.load(response)

        # Store title and authors information in book_data dictionnary
        volume_info = data_raw['items'][0]['volumeInfo']
        title = volume_info['title']
        authors = volume_info['authors']
        prettify_author = authors if len(authors) > 1 else authors[0]
        book_data = {'isbn': isbn, 'title': title, 'authors': prettify_author}

        # Add user if they have read the book and store the answer
        book_data['read'] = book_info_user.has_been_read()

        # If the book has been read, ask for a rating
        if book_data['read'] == 'true':
            book_data['rating'] = book_info_user.rate_book()
        # If the book has not been read, set rating to None
        else:
            book_data['rating'] = None

        # Add book to the database
        book_added = manage_database.add_book(conn, cur, book_data)
        # Print collected information
        if book_added:
            print("The following information has been added to the database:")
            print(book_data)

    # Ask user if they would like to add another book
    while True:
        user_update = input(
            'Would you like to enter another ISBN? yes or no '
            ).lower().strip()

        # Stop asking when the answer is 'yes' or 'no'
        if user_update == 'yes' or user_update == 'no':
            break

    # Break out of the loop
    if user_update == 'no':
        break

# Close communication with the database
manage_database.db_close(conn, cur)
