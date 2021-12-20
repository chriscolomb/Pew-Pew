from player import Player
import mongodb
class EditDatabase:
    
    def createPlayer(user):
        """adds player to database"""
        for id in mongodb.player_collection.find({},
                                                    {"_id": 1, "rating": 0, "win_count": 0, "lose_count": 0, "win_streak": 0, "best_win_streak": 0, "main": None}):
            if id["_id"] == user:
                #await message.channel.send("<@{0}> is already in the database.".format(user))
                print("already in database")
                return

        p1 = Player(user)
        p1_entry = {
            "_id": p1.id,
            "rating": p1.rating,
            "win_count": p1.win_count,
            "lose_count": p1.lose_count,
            "win_streak": p1.win_streak,
            "best_win_streak": p1.best_win_streak,
            "main":p1.main
        }
        mongodb.player_collection.insert_one(p1_entry)