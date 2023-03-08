from configparser import ConfigParser

def config(filename = 'database.ini', section = 'postgresql'):
    """ Retrieve information from database.ini to connect to the database """
    # Create a parser
    parser = ConfigParser()
    # Read config file
    parser.read(filename)

    # Get information from the right section, default being PostgreSQL
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db