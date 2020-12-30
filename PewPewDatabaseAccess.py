



def write_database(username):
    user = username

    def create_table(cursor):
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

    def add_primary_key():
    # add table entry
    user = username
    wins = 0
    losses = 0
    value = round(wins / (wins + losses), 4)

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

    def update_values_columuns():
    # modify entries
    user = 'DamagedTwitch'
    wins = 10
    losses = 5
    value = round(wins / (wins + losses), 4)

    profile_data = {
        'User': user,
        'Value': value,
        'Wins': wins,
        'Losses': losses,
    }
    update_user_wins = ("UPDATE Profile set Wins = %s "
                        "where user = %s")
    update_user_value = ("UPDATE Profile set Value = %s "
                         "where user = %s")

    cursor.execute(update_user_wins, (wins, user))
    cursor.execute(update_user_value, (value, user))
    conn.commit()

    cursor.close()
    conn.close()