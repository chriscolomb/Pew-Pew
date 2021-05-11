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
# ---------------------------------------------------------------------------------------------------------------------
# updates the usernames database columns and other update column methods that follow
def edit_username_score(conn, username, score):
    """edit the usernames score
    :param: conn: connection object
    :param: username: player to be edited
    :param: score: the score to add"""

    c = conn.cursor()
    edit_ranking = '''UPDATE players
                      SET ranking = ?
                      WHERE username = ?'''
    c.execute(edit_ranking, (score, username))


def edit_username_win_streak(conn, username, win_streak):
    """updates the other columns of players table
    :param: conn: connection object
    :param: username: player to be edited
    :param: win_streak: the username's win streak """


def edit_username_lose_streak(conn, username, lose_streak):
    """updates the other columns of players table
    :param: conn: connection object
    :param: username: player to be edited
    :param: win_streak: the username's win streak """


def edit_username_season_start(conn, username, start_season_rank):
    """updates the other columns of players table
    :param: conn: connection object
    :param: username: player to be edited
    :param: start_season_rank: the username's start of the season rank"""


def edit_username_season_end(conn, username, end_season_rank):
    """updates the other columns of players table
    :param: conn: connection object
    :param: username: player to be edited
    :param: end_season_rank: the username's end of the season rank"""
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

def edit_permissions(conn_p, username, add):
    """edits the permissions of the username, this is for getting admins when bot joins discord
    :param: conn_p: the connections object of permission database
    :param: username: the username to be edited
    :param: add: the boolean expression, whether the user will be added or removed]
    :returns: 1 if mod, and 2 if none"""

    update_permissions = '''UPDATE permissions
                            SET permission = ? WHERE username = ?'''
    username_permission = 2
    if add:
        username_permission = 1
    elif not add:
        username_permission = 2
    else:
        print("this isn't a valid argument")
    c_p = conn_p.cursor()
    c_p.execute(update_permissions, (username_permission, username))
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

def edit_win_percentage(conn_m, username):
    """calculates the win percentage
    :param conn_m: the connection object of the milestones table
    :param username: the user that needs the win percentage calculated
    :return: the calculated win percentage
    """
    c_m = conn_m.cursor()
    win_percentage_statement = '''UPDATE milestones
                               SET win_percentage = ?
                               WHERE username = ?'''
    wins = get_wins(conn_m, username)
    losses = get_losses(conn_m, username)
    calculate_win_percentage = round((wins/(wins+losses))*100, 4)
    c_m.execute(win_percentage_statement, (calculate_win_percentage,username))
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

def edit_biggest_win(conn_m, username):
    """
    :param conn_m:
    :param username:
    :return:
    """
def edit_reverse_3_stock_count(conn_m, username):
    """
    :param conn_m:
    :param username:
    :return:
    """
def edit_highest_rank(conn_m, username):
    """
    :param conn_m:
    :param username:
    :return:
    """
def edit_highest_win_streak(conn_m, username):
    """
    :param conn_m:
    :param username:
    :return:
    """

# start of get/view methods
def get_last_update(conn,username):
    """
    :param conn:
    :param username:
    :return:
    """
def get_win_streak(conn,username):
    """
    :param conn:
    :param username:
    :return:
    """
def get_start_season_rank(conn,username):
    """
    :param conn:
    :param username:
    :return:
    """
def get_end_season_rank(conn,username):
    """
    :param conn:
    :param username:
    :return:
    """

def get_report_points(conn,username):
    """returns the amount of points of the given username
    :param conn: the connection object to the database
    :param username:  the username to get the amount of points returned
    :return: points: the points to be returned to the given username
    """

def rank(conn, username):
    """returns the player's rank
    :param: conn: connection object
    :param: username: the player/username that needs the rank retrieved"""
    select_statement = '''SELECT ranking 
                          FROM players
                          WHERE username =?
                          '''
    # looks through database.
    # gets the ranking of the player but will be a tuple.
    # changes tuple to int.
    c = conn.cursor()
    c.execute(select_statement, (username,))
    the_ranking = c.fetchone()
    the_ranking_int = functools.reduce(lambda sub, ele: sub * 10 + ele, the_ranking)
    return int(the_ranking_int)


def get_permission(conn_p, username):
    """ returns the permission of the username
    :param conn_p: the connection object of the permissions table
    :param username: the user that needs the permission returned
    :return: the user's permission
    """
    select_statement = '''SELECT permission 
                          FROM permissions
                          WHERE username =?
                          '''
    c_p = conn_p.cursor()
    c_p.execute(select_statement, (username,))
    permission = c_p.fetchone()
    permission_int = int(functools.reduce(lambda sub, ele: sub * 10 + ele, permission))
    return permission_int


def get_wins(conn_m, username):
    """ returns the number of wins of a user
    :param conn_m: the connection object of the milestones database
    :param username: the username that needs the wins returned
    :return:
    """
    select_statement = '''SELECT wins 
                          FROM milestones
                          WHERE username =?
                          '''
    c_m = conn_m.cursor()
    c_m.execute(select_statement, (username,))
    the_wins = c_m.fetchone()
    num_of_wins = functools.reduce(lambda sub, ele: sub * 10 + ele, the_wins)
    return float(num_of_wins)


def get_losses(conn_m, username):
    """ returns the number of wins of a user
    :param conn_m: the connection object of the milestones database
    :param username: the username that needs the losses returned
    :return:
    """
    select_statement = '''SELECT losses 
                        FROM milestones
                        WHERE username =?
                        '''
    c_m = conn_m.cursor()
    c_m.execute(select_statement, (username,))
    the_losses = c_m.fetchone()
    num_of_losses = functools.reduce(lambda sub, ele: sub * 10 + ele, the_losses)
    return float(num_of_losses)

def get_win_percentage(conn_m, username):
    """
    :param conn_m:
    :param username:
    :return:
    """
def get_biggest_win(conn_m,username):
    """
    :param conn_m:
    :param username:
    :return:
    """
def get_reverse_3_stock_count(conn_m, username):
    """
    :param conn_m:
    :param username:
    :return:
    """

def get_highest_rank(conn_m, username):
    """
    :param conn_m:
    :param username:
    :return:
    """
def get_highest_win_streak(conn_m, username):
    """
    :param conn_m:
    :param username:
    :return:
    """
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# admin only methods,  maybe add a edit column and row methods for admins
def delete_username(conn, conn_p, username, to_delete):
    """deletes user from database
    :param: conn: connection object
    :param: username: the player/username that needs the rank retrieved"""
    username_permission = get_permission(conn_p, username)
    if username_permission == 0:
        delete_statement = '''DELETE FROM players
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


def undo_last_ranking(conn, conn_p, conn_m, username, undo_user):
    """the score received from ELO is given back to the users, if there is a mistake, the last_update will be recorded
    only if the users report the game. A mod can review and then use this method.
    :param: conn: the object for players database
    :param: conn_p: the object for permissions database
    :param: username: the username that is initiating the undo
    :param: undo_user: the username that needs the points undone"""
    revert_wins = True
    revert_loss = True
    if 0 <= get_permission(conn_p, username) < 3:
        select_statement = '''SELECT report_points 
                              FROM players
                              WHERE username =?
                              '''
        c = conn.cursor()
        c.execute(select_statement, (undo_user,))
        tuple_report = c.fetchone()
        report_points = int(functools.reduce(lambda sub, ele: sub * 10 + ele, tuple_report))
        player_pts = rank(conn, undo_user)
        updated_pts = player_pts - report_points
        edit_username_score(conn, undo_user, updated_pts)

        if report_points < 0:
            add_loss(conn_m, username, revert_loss)
        elif report_points > 0:
            add_wins(conn_m, username, revert_wins)
        else:
            print('something went wrong with removing or adding wins')


# testing methods below get players to check if it's correct
def get_permissions_table(conn_p):
    sql = '''   SELECT * 
                FROM permissions'''

    c_p = conn_p.cursor()
    c_p.execute(sql)
    print(c_p.fetchall())


def get_players_table(conn):
    sql = '''   SELECT * 
                FROM players'''

    c = conn.cursor()
    c.execute(sql)
    print(c.fetchall())


def get_milestones_table(conn_m):
    sql = '''   SELECT * 
                FROM milestones'''
    c_m = conn_m.cursor()
    c_m.execute(sql)
    print(c_m.fetchall())


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
        placeholder_players_tuple = (test_player, test_ranking, 0, 6, 0, 0, 0, 0)
        test_2_placeholder = ('player', new_ranking, 0, 0, 0, 0, 0, 0)
        add_username(conn, placeholder_players_tuple)
        add_username(conn, test_2_placeholder)

        edit_username_score(conn, test_player, new_ranking)
        the_rank = rank(conn, test_player)
        print('rank of TeamDuck {rnk}'.format(rnk=the_rank))

    else:
        print('There was an error establishing database connection.')

    if conn_p is not None:
        create_permissions_table(conn_p, permissions_table)
        moder_number = 2
        admin = 0
        # this would be for admins of guilds/servers
        moder_lead_number = 1
        test_user = 'glabber'
        test_server_admin = 'I am demi-god'
        admin_test = "godly"

        # permissions TESTS
        per = get_permission(conn_p, 'TeamDuck#0876')
        print('permissions of TeamDuck is {per}'.format(per=per))
        add_permissions_username(conn_p, 'TeamDuck#0876', test_user, moder_number)
        add_permissions_username(conn_p, 'TeamDuck#0876', test_server_admin, moder_lead_number)
        delete_mod(conn_p, test_user, test_server_admin)
        undo_last_ranking(conn, conn_p, conn_m, 'TeamDuck#0876', 'TeamDuck')
        insert_admins(conn_p, 'TeamDuck#0876', admin_test, admin)
        delete_username(conn, conn_p, 'TeamDuck#0876', 'player')
        # delete_admin(conn_p, 'TeamDuck#0876', 'DamagedTwitch#9044')
        add_fake_admin(conn_p, 'dingle')
    else:
        print("there is an error establishing the permissions database")

    if conn_m is not None:
        create_milestone_table(conn_m, milestone_table)
        test_user = 'DamagedTwitch#9044'
        tuple_user = (test_user, 1.0, 2.0, 0.0, 4, 5, 6, 7)
        add_milestone_user(conn_m, tuple_user)
        edit_win_percentage(conn_m, test_user)

        get_milestones_table(conn_m)
        get_permissions_table(conn_p)
        get_players_table(conn)


if __name__ == '__main__':
    main()
