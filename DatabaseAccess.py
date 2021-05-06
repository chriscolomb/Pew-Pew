import sqlite3


class Database:
    def __init__(self, player, score):
        self.player = player
        self.score = score

    # c.execute("""CREATE TABLE players (
    #             player text,
    #             ranking real
    #             )""")
    #
    # conn.commit()
    # opens the connections to the database and creates a cursor.

    def retrieveUser(self, player):
        conn = sqlite3.connect('players.db')
        c = conn.cursor()
        c.execute("""
        SELECT player 
        FROM 
            players 
        WHERE 
            player= (:player)
            """, {'player': player})
        self.player =c.fetchone()
        # print(self.player)


    def editUser(self,newScore):
        self.score = newScore
        print(self.score)
        conn = sqlite3.connect('players.db')
        c = conn.cursor()
        c.execute("""
        UPDATE
            players
        SET
            ranking = ?
        WHERE
            player = ?
            """, (self.score, self.player))

        c.fetchall()
        return 0

    # creats a new database for mod privilages.
    def assignModRole(self):
        return 0

    def makemodDB(self):
        return 0

    def viewRank(self):
        return

    def addUser(self):
        conn = sqlite3.connect('players.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO
                Players
            Values
                (:player, :score)
        """, {'player': self.player, 'score': self.score})

        conn.commit()
        c.execute("""
        SELECT * 
        FROM 
            players 
        WHERE 
            player= (:player)
            """, {'player': self.player})

        print(c.fetchone())
        conn.close()

    # for testing purposes
    def editRank(self):
        return 0

    def undoLastRanking(self, player2, points1, points2):
        return 0

    # only for testing purposes
    def clear(self):
        return 0


