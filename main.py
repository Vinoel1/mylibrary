import json
from urllib.request import urlopen
import book_info_user
import manage_database

# Connect to the database
conn, cur = manage_database.db_connect()

while True:
    # Send a request to the Google Books API
    api = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'
    # isbn = input('Enter a 10 or 13 digit ISBN: ').strip()
    # Test ISBN
    isbn = '9782823872118'
    response = urlopen(api + isbn)
    # Store JSON response in a dictionary
    data_raw = json.load(response)
    # print(data_raw)

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
    manage_database.add_book(conn, cur, book_data)

    # Ask user if they would like to add another book
    while True:
        user_update = input(
            'Would you like to enter another ISBN? yes or no '
            ).lower().strip()

        # Stop asking when the answer is 'yes' or 'no'
        if user_update == 'yes' or user_update == 'no':
            break

    # Print collected information and break out of the loop
    if user_update == 'no':
        print(book_data)
        break

# Close communication with the database
manage_database.db_close(conn, cur)
