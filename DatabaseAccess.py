import sqlite3
from sqlite3 import Error
import functools


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


def create_permissions_connection(db_file_p):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file_p: database file for permissions
    :return: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file_p)
        return conn
    except Error as e:
        print(e)

    return conn


def create_milestones_connection(db_file_m):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file_m)
        return conn
    except Error as e:
        print(e)

    return conn


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# create all tables
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_permissions_table(conn_p, permissions_table):
    """ create a permission table from the permission_table statement
    :param permissions_table: a permissions, CREATE TABLE statement
    :param conn_p: Connection object
    :return:
    """
    # the admin usernames for the table
    admin_username1 = 'TeamDuck#0876'
    admin_username2 = 'DamagedTwitch#9044'
    admin = 0
    row = '''   INSERT INTO permissions(username,permission)
                VALUES(?, ?)'''
    error = False

    try:
        c_p = conn_p.cursor()
        c_p.execute(permissions_table)
    except Error as e:
        print(e)
        error = True

    if not error:
        c_p.execute(row, (admin_username1, admin))
        c_p.execute(row, (admin_username2, admin))


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


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# add usernames to tables and other add (insert) methods that follow
def add_username(conn, placeholder):
    """ Adds username into the players table
    :param conn: the conn object for players database
    :param placeholder: the tuple for username plus stats
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


def add_fake_admin(conn_p, username):
    """ the function that gives 'mod admin' to owners of other servers
    :param conn_p: the permissions database object
    :param username: the user to be added to the database, permissions
    :return:
    """
    fake_admin = 1
    row = '''   INSERT INTO permissions(username,permission)
                    VALUES(?, ?)'''
    c_p = conn_p.cursor()
    c_p.execute(row, (username, fake_admin))
    conn_p.commit()


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

def add_wins(conn_m, username, negative):
    """ adds a win to user
    :param conn_m: connection object to the milestones table
    :param username: the username to add wins
    :param negative: a boolean the dictates if the value will be subtracted or added
    :return:
    """


def add_loss(conn_m, username, negative):
    """add's a loss to a user
    :param conn_m: connection object to the milestones table
    :param username: the username to add a loss
    :param negative: a boolean the dictates if the value will be subtracted or added
    :return:
    """


# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------

def update_win_percentage(conn_m, username, column_w, column_l, column, table):
    """calculates the win percentage and updates the win percentage
    :param table: the table that the columns are in
    :param column:  column that is win percentage
    :param column_l: the column that is losses
    :param column_w:  the column that is wins
    :param conn_m: the connection object of the milestones table
    :param username: the user that needs the win percentage calculated
    :return: none
    """
    c_m = conn_m.cursor()
    win_percentage_statement = '''UPDATE ''' + table + '''
                               SET ''' + column + ''' = ?
                               WHERE username = ?'''
    wins = get_column_value(conn_m, username, column_w, table)
    losses = get_column_value(conn_m, username, column_l, table)
    calculate_win_percentage = round((wins / (wins + losses)) * 100, 4)
    c_m.execute(win_percentage_statement, (calculate_win_percentage, username))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

def update_column(conn, username, column, table, value):
    """ updates the column given with the value
    :param conn: connection object
    :param username: the username to update
    :param column: the column to be updated
    :param table: the table that has the column
    :param value:  the value to be updated
    :return: None
    """
    update_statement = '''UPDATE ''' + table + '''
                          SET ''' + column + ''' = ?
                          WHERE username = ?'''
    c = conn.cursor()
    c.execute(update_statement, (value, username))


# start of get/view methods
def get_column_value(conn, username, column, table):
    """returns the column value in a given table
    :param conn: connection object
    :param username: the player/username that needs the column retrieved
    :param column: the column
    :param table: the table that the column is in"""
    select_statement = '''SELECT ''' + column + ''' 
                          FROM ''' + table + '''
                          WHERE username =?
                          '''

    # looks through database.
    # gets the column value of the player but will be a tuple.
    # changes tuple to int.
    c = conn.cursor()
    c.execute(select_statement, (username,))
    column_tuple = c.fetchone()
    column_value = functools.reduce(lambda sub, ele: sub * 10 + ele, column_tuple)
    return int(column_value)


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# admin only methods,  maybe add a edit column and row methods for admins
def delete_username(conn, conn_p, username, to_delete, table, column_permissions, table_permissions,):
    """deletes user from database
    :param conn: connection object
    :param conn_p:
    :param username: the admin/mod that is doing the deletion
    :param to_delete: the user that is to be deleted
    :param table: the players table
    :param column_permissions: the column in permissions
    :param table_permissions:  the table for permissions
    :return: none
    """
    """
    :param: conn: 
    :param: username: the player/username that needs the rank retrieved"""
    username_permission = get_column_value(conn_p, username, column_permissions, table_permissions)
    if username_permission == 0:
        delete_statement = '''DELETE FROM ''' + table + '''
                              WHERE username = ?'''
        c = conn.cursor()
        c.execute(delete_statement, (to_delete,))


# not sure if we should add this
def insert_admins(conn_p, username, to_add, admin):
    """deletes admins from admin list, only admin can access this
    :param: conn_p: the permissions
    :param: username: the username that's the admin
    :param: to_add: the username that is to be added as an admin"""
    username_permission = get_permission(conn_p, username)
    if username_permission == 0:
        row = '''   INSERT OR IGNORE INTO permissions(username,permission)
                    VALUES(?, ?)'''
        c_p = conn_p.cursor()
        c_p.execute(row, (to_add, admin))
        conn_p.commit()


# not sure if this method is actually needed, unless we decide to promote someone.
def delete_admin(conn_p, username, to_delete):
    """deletes admin from database
    :param: conn: connection object
    :param: yo_delete: the player/username that needs to be deleted
    :param: username: the player/username that is trying to delete"""
    username_permission = get_permission(conn_p, username)
    if username_permission == 0:
        delete_statement = '''DELETE FROM permissions
                           WHERE username = ?'''
        c_p = conn_p.cursor()
        c_p.execute(delete_statement, (to_delete,))


# mod and admin only methods below
def add_permissions_username(conn_p, username, add_user, mod_number):
    """adds user as mods to the table permissions
    :param: conn_p: the permissions table object
    :param: username: the username adding mod privilege
    :param: add_user: the username to be added to mod
    :param: mod_number: the number that represents server admin (not main server)"""
    permissions = get_permission(conn_p, username)
    if permissions < 1:
        row = '''   INSERT OR IGNORE INTO permissions(username,permission)
                    VALUES(?, ?)'''
        c_p = conn_p.cursor()
        c_p.execute(row, (add_user, mod_number))
        conn_p.commit()


def delete_mod(conn_p, username, to_delete):
    """deletes moderator from database
    :param: conn_p: connection object
    :param: yo_delete: the player/username that needs to be deleted
    :param: username: the player/username that is trying to delete"""
    test_if_admin = get_permission(conn_p, to_delete)
    username_permission = get_permission(conn_p, username)
    if username_permission < test_if_admin:
        delete_statement = '''DELETE FROM permissions
                           WHERE username = ?'''
        c_p = conn_p.cursor()
        c_p.execute(delete_statement, (to_delete,))


# Have to incorporate undo wins/loses too
# This will see if last_update is negative or positive and revert the loss or win
#
#


def undo_last_ranking(conn, conn_p, conn_m, username, undo_user, column, table, column_players, table_players):
    """the score received from ELO is given back to the users, if there is a mistake, the last_update will be recorded
    only if the users report the game. A mod can review and then use this method.
    :param table_players: the players table, to be updated
    :param column_players:  the username to be undone, column; in the table in "table_players"
    :param conn_m: database object for milestones
    :param table: the table for permissions
    :param column: the column in permissions database
    :param conn: the object for players database
    :param conn_p: the object for permissions database
    :param username: the username that is initiating the undo
    :param undo_user: the username that needs the points undone"""
    revert_wins = True
    revert_loss = True
    if 0 <= get_column_value(conn_p, username, column, table) < 3:
        select_statement = '''SELECT ''' + column_players + '''
                              FROM ''' + table_players + '''
                              WHERE username =?
                              '''
        c = conn.cursor()
        c.execute(select_statement, (undo_user,))
        tuple_report = c.fetchone()
        report_points = int(functools.reduce(lambda sub, ele: sub * 10 + ele, tuple_report))
        player_pts = get_column_value(conn, undo_user, column_players, table_players)
        updated_pts = player_pts - report_points
        update_column(conn, undo_user, column_players, table_players, updated_pts)

        if report_points < 0:
            add_loss(conn_m, username, revert_loss)
        elif report_points > 0:
            add_wins(conn_m, username, revert_wins)
        else:
            print('something went wrong with removing or adding wins')


# testing methods below get players to check if it's correct
def get_table(conn, table):
    sql = '''   SELECT * 
                FROM ''' + table

    c = conn.cursor()
    c.execute(sql)
    print(c.fetchall())


# might be good to make a table for a string variable, for similar methods. instead of having multiple methods.
# a SELECT variable
# a FROM variable
# a SET variable
# a table variable, to possibly clean up code but could get confusing with method names. but delete username and insert
# may be able to be combined
# not sure if this is even possible...

# can create a database object for the stuff below
def main():
    db_file = ':memory:'
    permissions_db_file = ':memory:'
    milestone_db_file = ':memory:'

    players_table = """ CREATE TABLE IF NOT EXISTS players (
                        username text PRIMARY KEY,
                        ranking integer NOT NULL,
                        last_update integer NOT NULL,
                        report_points integer NOT NULL,
                        win_streak integer NOT NULL,
                        lose_streak integer Not NULL,
                        start_season_rank integer NOT NULL,
                        end_season_rank integer NOT NULL                        
                        ); """

    permissions_table = """ CREATE TABLE IF NOT EXISTS permissions (
                            username text PRIMARY KEY,
                            permission integer NOT NULL
                            ); """
    milestone_table = '''CREATE TABLE IF NOT EXISTS milestones (
                        username text PRIMARY KEY,
                        wins real NOT NULL,
                        losses real NOT NULL,
                        win_percentage real NOT NULL,
                        biggest_win integer NOT NULL,
                        reverse_3_stock_count integer NOT NULL,
                        highest_rank integer NOT NULL,
                        highest_win_streak integer NOT NULL
                        );'''

    # create db connection
    conn = create_connection(db_file)
    conn_p = create_permissions_connection(permissions_db_file)
    conn_m = create_milestones_connection(milestone_db_file)

    # create table (if needed)
    if conn is not None:
        create_table(conn, players_table)
        # TESTS
        test_player = 'TeamDuck'
        test_ranking = 2400
        new_ranking = 2100
        get_column = 'ranking'
        table = 'players'
        placeholder_players_tuple = (test_player, test_ranking, 0, 6, 0, 0, 0, 0)
        add_username(conn, placeholder_players_tuple)
        get_table(conn, table)
        update_column(conn, test_player, table, get_column, new_ranking)
        get_column_value(conn, test_player, get_column, table)
        get_table(conn, table)


    else:
        print('There was an error establishing database connection.')

    if conn_p is not None:
        create_permissions_table(conn_p, permissions_table)
        admin = 0
        fake_admin = 1
        moder_number = 2
        test_user = 'glabber'
        test_server_admin = 'I am demi-god'
        admin_test = "godly"

    else:
        print("there is an error establishing the permissions database")

    if conn_m is not None:
        create_milestone_table(conn_m, milestone_table)


if __name__ == '__main__':
    main()
