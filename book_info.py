""" Parse information given by the API and ask user for their personnal
information about the book """

def parse_raw(isbn, data_raw):
    """ Store title and authors information in book_data dictionnary """
    volume_info = data_raw['items'][0]['volumeInfo']
    title = volume_info['title']
    authors_raw = volume_info['authors']
    authors = [author.title() for author in authors_raw]
    book_data = {'isbn': isbn, 'title': title}

    return book_data, authors


def has_been_read():
    """ Ask user if they have read the book then return the answer"""
    while True:
        read_status = input(
            'Have you read this book? true or false '
            ).lower().strip()

        # Stop asking when the answer is 'true' or 'false'
        if read_status in {'true', 'false'}:
            break

    return read_status


def rate_book():
    """ Ask user for a rating from 0 to 5 then return the rating"""
    while True:
        # Ask until the rating is a number from 0 to 5
        try:
            rating = int(input('Rate this book from 0 to 5: ').strip())
        # If the given value is not an integer, ask for a rating again
        except ValueError:
            print('Please enter a number from 0 to 5')
            continue

        # If the given value is not correct, ask for a rating again
        if rating < 0 or rating > 5:
            print('Please enter a number from 0 to 5')
            continue
        # If the given value is correct, break out of the loop
        break

    return rating


def ask_if_read_and_rate(book_data):
    """ Ask user if they have read the book and if they have,
    ask for a rating """
    # Ask user if they have read the book and store the answer
    book_data['read'] = has_been_read()

    # If the book has been read, ask for a rating
    if book_data['read'] == 'true':
        book_data['rating'] = rate_book()
    # If the book has not been read, set rating to None
    else:
        book_data['rating'] = None

    return book_data
