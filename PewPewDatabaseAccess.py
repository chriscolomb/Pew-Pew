import mysql.connector
from mysql.connector import errorcode


# access to SQL database, can update this later to include other fights (new table)
# can create a new table for different fights and make a change in the DB, maybe DB name should
# be passed to the methods.

def create_table(table_name):
    # connect to database
    conn = None
    conn = mysql.connector.connect(
        host='130.211.119.74',
        user='root',
        password='togcow-nuvgyQ-7fydme',
        database='PewPew'
    )
    if conn.is_connected():
        print('Connected to MySQL database')
    cursor = conn.cursor(buffered=True)

    # creates table
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
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    cursor.close()
    conn.close()


def add_primary_key(username):
    # connect to database
    conn = None
    conn = mysql.connector.connect(
        host='130.211.119.74',
        user='root',
        password='togcow-nuvgyQ-7fydme',
        database='PewPew'
    )
    if conn.is_connected():
        print('Connected to MySQL database')
    cursor = conn.cursor(buffered=True)

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
        cursor.execute(conn_query, profile_data)
    except mysql.connector.errors.IntegrityError:
        # other errors can happen but not to figure out this try except statement.
        print('The user already exist')

    conn.commit()

    cursor.close()
    conn.close()


def update_values_columns(username, WorL):
    # connect to database
    conn = None
    conn = mysql.connector.connect(
        host='130.211.119.74',
        user='root',
        password='togcow-nuvgyQ-7fydme',
        database='PewPew'
    )
    if conn.is_connected():
        print('Connected to MySQL database')
    cursor = conn.cursor(buffered=True)

    # modify entries
    user = username
    result = ()
    location = """select * from Profile where user = %s"""

    if WorL == 'w':
        result = ("UPDATE Profile set Wins = Wins + 1 "
                  "where user = %s")
    elif WorL == 'l':
        result = ("UPDATE Profile set Losses = Losses + 1 "
                  "where user = %s")
    else:
        print("there is something wrong, error")

    cursor.execute(location, (user,))
    cursor.execute(result, (user,))
    conn.commit()

    # prints the user updated and the row of the user (primary key, I think it's called)
    cursor.execute(location, (user,))
    results = cursor.fetchall()
    if cursor.rowcount > 0:
        print(cursor.rowcount, "record(s) affected")
        for x in results:
            print(x)
    else:
        print('no records affected')
    cursor.close()
    conn.close()


def get_user_value(username):
    print('function for getting value of username, wins loses')
    # returns a value that can be turned into percent.
