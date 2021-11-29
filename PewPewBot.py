import discord
import MongoDB
from Player import Player

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user.name))

    # async def on_message(self, message, member:discord.Member):
    #     print("someone was pinged")
    #     if message.content == "!match":
    #         await message.channel.send("test")
    #         if member == None:
    #             await message.channel.send("To match with someone, use `!match @player`.")

    #         elif member != None:
    #             await message.channel.send("Starting match with {0}!".format(member))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.content == "!create":
            # print("test command received")
            for id in MongoDB.player_collection.find({},
                                                     {"_id": 1, "rating": 0, "win_count": 0, "lose_count": 0, "win_streak": 0, "best_win_streak": 0}):
                if id["_id"] == message.author.id:
                    await message.channel.send("<@{0.author.id}> is already in the database.".format(message))
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
            MongoDB.player_collection.insert_one(p1_entry)
            await message.channel.send("<@{0.author.id}> entry for database created.".format(message))


        elif message.content == "!delete":
            for id in MongoDB.player_collection.find({},
                                                     {"_id": 1, "rating": 0, "win_count": 0, "lose_count": 0, "win_streak": 0, "best_win_streak": 0}):
                if id["_id"] == message.author.id:
                    delete_id = {"_id": message.author.id}
                    MongoDB.player_collection.delete_one(delete_id)
                    await message.channel.send("Entry for <@{0.author.id}> has been deleted.".format(message))
                    return

            await message.channel.send("<@{0.author.id}> is not in the database.".format(message))

        elif message.content == "!stats":
            for id in MongoDB.player_collection.find():
                if id["_id"] == message.author.id:
                    title = "Stats for {0.author}".format(message)

                    embed = discord.Embed(
                        title = title,
                        colour = discord.Colour.green()
                    )

                    embed.add_field(name="Rating", value=id.get("rating"))
                    embed.add_field(name="Win Count", value=id.get("win_count"))
                    embed.add_field(name="Lose Count", value=id.get("lose_count"))
                    embed.add_field(name="Win Streak", value=id.get("win_streak"))
                    embed.add_field(name="Best Win Streak", value=id.get("best_win_streak"))

                    await message.channel.send(embed = embed)
                    return

            await message.channel.send("<@{0.author.id}> is not in the database.".format(message))









client = MyClient()
client.run('NzkwNzg0MzU0NTgxNzQxNTk5.X-FpUg.AfDsH6U1x5GNlE_1tjGwmjjuNVU')