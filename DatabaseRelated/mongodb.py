import pymongo
from pprint import pprint


from pymongo import collection # pprint library is used to make the output look more pretty

# connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://teamduckssb:em-xJFw-97G5mpG@testing-cluster.rzshs.mongodb.net/test")
bot_db = client["Bot"]
player_collection = bot_db["Player"]
battle_collection = bot_db["BattleInProgress"]
# Issue the serverStatus command and print the results
serverStatusResult=bot_db.command("serverStatus")
#pprint(serverStatusResult)

db_list = client.list_database_names()
collection_list = bot_db.list_collection_names()