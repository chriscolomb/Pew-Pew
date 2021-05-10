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
        c = conn_m.cursor()
        c.execute(milestone_table)
    except Error as e:
        print(e)


# add usernames to tables
def add_username(conn, placeholder):
    sql = '''INSERT INTO players(username,ranking, last_update,report_points, win_streak,lose_streak, start_season_rank, 
                                 end_season_rank) VALUES(?,?,?,?,?,?,?,?)'''

    c = conn.cursor()
    c.executemany(sql, (placeholder,))
    conn.commit()


# updates the usernames database columns
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


# will be completed after initial release
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


# edit the permissions of user
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


def view_permission(conn_p, username):
    select_statement = '''SELECT permission 
                          FROM permissions
                          WHERE username =?
                          '''
    c_p = conn_p.cursor()
    c_p.execute(select_statement, (username,))
    permission = c_p.fetchone()
    permission_int = int(functools.reduce(lambda sub, ele: sub * 10 + ele, permission))
    return permission_int


# may change this to view and add a table and column parameter
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


# other view files would go hear, ones the retrieve milestone stats and such


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


# admin only methods,  maybe add a edit column and row methods for admins
def delete_username(conn, conn_p, username, to_delete):
    """deletes user from database
    :param: conn: connection object
    :param: username: the player/username that needs the rank retrieved"""
    username_permission = view_permission(conn_p, username)
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
    username_permission = view_permission(conn_p, username)
    if username_permission == 0:
        row = '''   INSERT INTO permissions(username,permission)
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
    username_permission = view_permission(conn_p, username)
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
    permissions = view_permission(conn_p, username)
    if permissions < 1:
        row = '''   INSERT INTO permissions(username,permission)
                    VALUES(?, ?)'''
        c_p = conn_p.cursor()
        c_p.execute(row, (add_user, mod_number))
        conn_p.commit()


def delete_mod(conn_p, username, to_delete):
    """deletes moderator from database
    :param: conn_p: connection object
    :param: yo_delete: the player/username that needs to be deleted
    :param: username: the player/username that is trying to delete"""
    test_if_admin = view_permission(conn_p, to_delete)
    username_permission = view_permission(conn_p, username)
    if username_permission < test_if_admin:
        delete_statement = '''DELETE FROM permissions
                           WHERE username = ?'''
        c_p = conn_p.cursor()
        c_p.execute(delete_statement, (to_delete,))


def undo_last_ranking(conn, conn_p, username, undo_user):
    """the score received from ELO is given back to the users, if there is a mistake, the last_update will be recorded
    only if the users report the game. A mod can review and then use this method.
    :param: conn: the object for players database
    :param: conn_p: the object for permissions database
    :param: username: the username that is initiating the undo
    :param: undo_user: the username that needs the points undone"""

    if 0 <= view_permission(conn_p, username) < 3:
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


# might be good to make a table for a string variable, for similar methods. instead of having multiple methods.
# a SELECT variable
# a FROM variable
# a SET variable
# a table variable, to possibly clean up code but could get confusing with method names. but delete username and insert
# may be able to be combined
# not sure if this is even possible...
def main():
    db_file = ':memory:'
    permissions_db_file = ':memory:'
    # future use
    milestone_db_file = ''

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
    # future use: milestone_table = '''Create TABLE IF NOT EXISTS milestones
    #                               wins
    #                               loses
    #                               win percentage
    #                               biggest win
    #                               reverse 3 stock count
    #                               highest rank
    #                               highest win streak'''

    # create db connection
    conn = create_connection(db_file)
    conn_p = create_permissions_connection(permissions_db_file)
    # future use: conn_m = create_milestones_connection(milestone_db_file):

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

        # get_players_table(conn)
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
        per = view_permission(conn_p, 'TeamDuck#0876')
        print('permissions of TeamDuck is {per}'.format(per=per))
        add_permissions_username(conn_p, 'TeamDuck#0876', test_user, moder_number)
        add_permissions_username(conn_p, 'TeamDuck#0876', test_server_admin, moder_lead_number)
        delete_mod(conn_p, test_user, test_server_admin)
        undo_last_ranking(conn, conn_p, 'TeamDuck#0876', 'TeamDuck')
        insert_admins(conn_p, 'TeamDuck#0876', admin_test, admin)
        delete_username(conn, conn_p, 'TeamDuck#0876', 'player')
        # delete_admin(conn_p, 'TeamDuck#0876', 'DamagedTwitch#9044')
        add_fake_admin(conn_p, 'dingle')

        get_permissions_table(conn_p)
        get_players_table(conn)
    else:
        print("there is an error establishing the permissions database")


if __name__ == '__main__':
    main()
