import mysql.connector
from mysql.connector import errorcode


def create_table(cursor_name, connection_name):
    DB_NAME = 'PewPew'
    TABLES = {}

    TABLES['Profile'] = (
        "CREATE TABLE `Profile` ("
        "  `User` varchar(37) NOT NULL,"
        "  `Value` float(20) NOT NULL,"
        "  `Wins` int(11) NOT NULL,"
        "  `Losses` int(11) NOT NULL,"
        "  PRIMARY KEY (`User`)"
        ") ENGINE=InnoDB")

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor_name.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        try:
            cursor_name.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    cursor_name.close()
    connection_name.close()


def add_primary_key(username, connection_name, cursor_name):
    # add table entry
    user = username
    wins = 0
    losses = 0
    value = 0

    conn_query = (
        "INSERT INTO `Profile` (`User`, `Value`, `Wins`, `Losses`)"
        "VALUES (%(User)s, %(Value)s, %(Wins)s, %(Losses)s)")
    profile_data = {
        'User': user,
        'Value': value,
        'Wins': wins,
        'Losses': losses,
    }

    # re-format this to cover other other error messages.
    try:
        cursor_name.execute(conn_query, profile_data)
    except mysql.connector.errors.IntegrityError:
        # other errors can happen but not to figure out this try except statement.
        print('The user already exist')

    connection_name.commit()

    cursor_name.close()
    connection_name.close()


def update_values_columns(username, connection_name, cursor_name, WorL):
    # modify entries
    user = username
    result = ()

    if WorL == 'w':
        result = ("UPDATE Profile set Wins = Wins + 1 "
                  "where user = user")
    elif WorL == 'l':
        result = ("UPDATE Profile set Losses = Losses + 1 "
                  "where user = user")
    else:
        print("there is something wrong, error")

    cursor_name.execute(result, user)
    connection_name.commit()
    cursor_name.close()
    connection_name.close()
