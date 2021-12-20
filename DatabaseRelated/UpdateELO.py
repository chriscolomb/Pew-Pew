import mongodb

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