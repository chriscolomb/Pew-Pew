import discord
import mongodb
from player import Player

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user.name))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.content == "!create":
            print("test command received")
            for id in mongodb.player_collection.find({},
            {"_id": 1, "rating": 0, "win_count": 0, "lose_count": 0, "win_streak": 0, "best_win_streak": 0}):
                for key in id:
                    if id[key] == message.author.id:
                        print("{0.author} is already in the database.".format(message))
                        return
            
            p1 = Player(message.author.id)
            p1_entry = {
                "_id": p1.id, 
                "rating": p1.rating, 
                "win_count": p1.win_count, 
                "lose_count": p1.lose_count, 
                "win_streak": p1.win_streak, 
                "best_win_streak": p1.best_win_streak
                }
            mongodb.player_collection.insert_one(p1_entry)
            print("{0.author} entry for database created.".format(message))
    
        
        elif message.content == "!delete":
            for id in mongodb.player_collection.find({},
            {"_id": 1, "rating": 0, "win_count": 0, "lose_count": 0, "win_streak": 0, "best_win_streak": 0}):
                for key in id:
                    if id[key] == message.author.id:
                        delete_id = {"_id": message.author.id}
                        mongodb.player_collection.delete_one(delete_id)
                        print("Entry for {0.author} has been deleted.".format(message))
                        return
            
            print("{0.author} is not in the database.".format(message))
                    
                        

client = MyClient()
client.run('NzkwNzg0MzU0NTgxNzQxNTk5.X-FpUg.AfDsH6U1x5GNlE_1tjGwmjjuNVU')

