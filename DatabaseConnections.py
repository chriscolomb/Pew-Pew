import DatabaseAccess
import sqlite3
from sqlite3 import Error
import functools


class DBConnections:

    def __init__(self, db_file):
        self.set__set_db_file(db_file)
        # maybe can use this to set admin if permission table is created
        # self.set__permission_admin


# creates all connections for table
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


# create all tables
def create_table(conn, create_table_sql, admin_table, permission_column, permission_table):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :param admin_table: if the table is a permissions table create the permissions admin
    :param permission_column: the column to add permission admin
    :return:
    """
    error = False
    # the admin usernames for the table
    if admin_table:
        admin_username1 = 'TeamDuck#0876'
        admin_username2 = 'DamagedTwitch#9044'
        admin = 0
        row = '''   INSERT INTO ''' + permission_table + '(username,' + permission_column + ''' )
                    VALUES(?, ?)'''
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

    if not error:
        c.execute(row, (admin_username1, admin))
        c.execute(row, (admin_username2, admin))


def create_permissions_table(conn_p, permissions_table):
    """ create a permission table from the permission_table statement
    :param permissions_table: a permissions, CREATE TABLE statement
    :param conn_p: Connection object
    :return:
    """

    try:
        c_p = conn_p.cursor()
        c_p.execute(permissions_table)
    except Error as e:
        print(e)
        error = True


def create_milestone_table(conn_m, milestone_table):
    """ create a milestone table from the milestone_table statement
    :param milestone_table: a permissions, CREATE TABLE statement
    :param conn_m: Connection object
    :return:
    """
    try:
        c_m = conn_m.cursor()
        c_m.execute(milestone_table)
    except Error as e:
        print(e)


# add usernames to tables and other add (insert) methods that follow
def add_username(conn, placeholder, num_of_columns):
    """ Adds username into the players table
    :param conn: the conn object for players database
    :param placeholder: the tuple for username plus stats
    :param num_of_columns: the number of columns to add
    :return:
    """
    insert_user = '''INSERT INTO players(username,ranking, last_update,report_points, win_streak,lose_streak, start_season_rank, 
                                 end_season_rank) VALUES(?,?,?,?,?,?,?,?)'''

    c = conn.cursor()
    c.executemany(insert_user, (placeholder,))
    conn.commit()


def add_milestone_user(conn_m, placholder_m):
    """Add a user to the milestone table
    :param conn_m: the connection object for milestones database
    :param placholder_m:
    :return:
    """
    insert_user = '''INSERT INTO milestones (username, wins, losses, win_percentage, biggest_win, 
                     reverse_3_stock_count, highest_rank, highest_win_streak) VALUES (?,?,?,?,?,?,?,?)'''

    c_m = conn_m.cursor()
    c_m.executemany(insert_user, (placholder_m,))


def add_fake_admin(conn, username, column, table, key):
    """ the function that gives 'mod admin' to owners of other servers
    :param conn: the permissions database object
    :param username: the user to be added to the database, permissions
    :param column: the column in permissions
    :param table: the table that is permissions
    :param key: the primary key of the table
    :return:
    """
    'username should be primary key'
    fake_admin = 1
    row = '''   INSERT OR IGNORE INTO ''' + table + '(' + key + ',' + column + ''')
                    VALUES(?, ?)'''
    c = conn.cursor()
    c.execute(row, (username, fake_admin))
    conn.commit()


def create_column(column_name, data_type, constraints):
    row = column_name + ' ' + data_type + ' ' + constraints
    return row
def all_columns():
    exit_loop = False
    while not exit_loop:

def add_username(conn, placeholder, table):
    """ Adds username into the players table
    :param conn: the conn object for players database
    :param placeholder: the tuple for username plus stats
    :param table: the table that the username will be added to
    :return:
    """
    # get a list of columns this way
    # get_column_names=con.execute("select * from table_name limit 1")
    # col_name=[i[0] for i in get_column_names.description]
    # print(col_name)
    placeholder.length()
    insert_user = '''INSERT INTO players(username,ranking, last_update,report_points, win_streak,lose_streak, start_season_rank, 
                                 end_season_rank) VALUES(?,?,?,?,?,?,?,?)'''

    c = conn.cursor()
    c.executemany(insert_user, (placeholder,))
    conn.commit()


def create_table(conn, create_table_sql, admin_table, permission_column, permission_table):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :param admin_table: if the table is a permissions table create the permissions admin
    :param permission_column: the column to add permission admin
    :return:
    """

    # the admin usernames for the table
    if admin_table:
        admin_username1 = 'TeamDuck#0876'
        admin_username2 = 'DamagedTwitch#9044'
        admin = 0
        row = '''   INSERT INTO ''' + permission_table + '(username,' + permission_column + ''' )
                    VALUES(?, ?)'''
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

    if admin_table:
        c.execute(row, (admin_username1, admin))
        c.execute(row, (admin_username2, admin))