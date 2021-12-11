import mongodb
'''Updates ELO ratings from match results'''
def update_elo_rating(winner, loser):
    # Get ratings from Player objects
    winner_rating = winner.get_rating()
    loser_rating = loser.get_rating()

    # Calculate probabilities of winning
    winner_probability = winner_rating / (winner_rating + loser_rating)
    loser_probability = loser_rating / (winner_rating + loser_rating)    

    p1_k = 16
    p2_k = 16
    # USCF K-factor
    if winner_rating >= 2400:
        if loser_rating >= 2400:
            p1_k = 16
            p2_k = 16
        elif loser_rating >= 2100:
            p1_k = 16
            p2_k = 24
        elif loser_rating < 2100:
            p1_k = 16
            p2_k = 32
    if loser_rating > 2400:
        if winner_rating >= 2100:
            p1_k = 24
            p2_k = 16
        elif winner_rating < 2100:
            p1_k = 32
            p2_k = 16

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