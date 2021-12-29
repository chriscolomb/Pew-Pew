import mongodb
from player import Player
from datetime import datetime as dt
'''Updates ELO ratings from match results'''
def update_elo_rating(winner, loser):
    # Get ratings from Player objects
    winner_rating = winner.rating
    loser_rating = loser.rating

    # Calculate probabilities of winning
    winner_probability = winner_rating / (winner_rating + loser_rating)
    loser_probability = loser_rating / (winner_rating + loser_rating)    

    # FIDE K-factor for Winner
    if winner_rating < 2300 or (winner.win_count + winner.lose_count) <= 30:
        p1_k = 40
    elif winner_rating < 2400:
        p1_k = 20
    else:
        p1_k = 10
    
    # FIDE K-factor for Loser
    if loser_rating < 2300 or (loser.win_count + loser.lose_count) <= 30:
        p2_k = 40
    elif loser_rating < 2400:
        p2_k = 20
    else:
        p2_k = 10

    # Calculate players' ELO ratings
    winner_rating = winner_rating + p1_k * (1 - winner_probability)
    loser_rating = loser_rating + p2_k * (0 - loser_probability)

    # Set new ratings to Player objects
    winner.set_rating(int(round(winner_rating,0)))
    loser.set_rating(int(round(loser_rating,0)))
    
    # Add wins and loses accordingly
    winner.plus_win()
    loser.plus_lose()

    p1_query = {
        "_id": winner.id,
    }
    new_p1 = { 
        "$set": { 
            "rating": winner.rating,
            "win_count": winner.win_count,
            "lose_count": winner.lose_count,
            "win_streak": winner.win_streak,
            "best_win_streak": winner.best_win_streak
        } 
    }

    p2_query = {
        "_id": loser.id,
    }
    new_p2 = { 
        "$set": { 
            "rating": loser.rating,
            "win_count": loser.win_count,
            "lose_count": loser.lose_count,
            "win_streak": loser.win_streak,
            "best_win_streak": loser.best_win_streak
        } 
    }

    mongodb.player_collection.update_one(p1_query, new_p1)
    mongodb.player_collection.update_one(p2_query, new_p2)

    #add battle to history collection
    history_entry = {
        "winner": winner.get_id(),
        "loser": loser.get_id(),
        "date": dt.now()
    }
    mongodb.history_collection.insert_one(history_entry)

    for player in mongodb.player_collection.find():
        if player["_id"] == winner.get_id():
            copy = player["match_history"]
            if player["match_history"][0].get(str(loser.get_id())) != None:
                copy[0][str(loser.get_id())] += 1
            else:                 
                copy[0][str(loser.get_id())] = 1    
            query = {
                "_id": winner.get_id(),
            }
            update_query = { "$set": { "match_history": copy } }
            mongodb.player_collection.update_one(query, update_query)
        elif player["_id"] == loser.get_id():
            copy = player["match_history"]
            if player["match_history"][1].get(str(winner.get_id())) != None:
                copy[1][str(winner.get_id())] += 1
            else:                 
                copy[1][str(winner.get_id())] = 1    
            query = {
                "_id": loser.get_id(),
            }
            update_query = { "$set": { "match_history": copy } }
            mongodb.player_collection.update_one(query, update_query)
