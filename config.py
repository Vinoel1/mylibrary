""" Read parameters in database.ini file """

import configparser


def config(filename = 'database.ini', section = 'postgresql'):
    """ Retrieve information from database.ini to connect to the database """
    # Create a parser
    parser = configparser.ConfigParser()
    # Read config file
    parser.read(filename)

    # Get information from the right section, default being PostgreSQL
    db_params = {}
    try:
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    except configparser.NoSectionError as error:
        print(error)

    return db_params
