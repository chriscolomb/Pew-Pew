'''Updates ELO ratings from match results'''
def update_elo_rating(p1, p2, p1_wins_bool):
    # Get ratings from Player objects
    p1_rating = p1.get_rating()
    p2_rating = p2.get_rating()
    
    # Calculate probabilities of winning
    p1_probability = p1_rating / (p1_rating + p2_rating)
    p2_probability = p2_rating / (p1_rating + p2_rating)

    # USCF K-factor
    if p1_rating > 2400:
        if p2_rating > 2400:
            p1_k = 16
            p2_k = 16
        elif p2_rating >= 2100:
            p1_k = 16
            p2_k = 24
        elif p2_rating < 2100:
            p1_k = 16
            p2_k = 32
    if p2_rating > 2400:
        if p1_rating >= 2100:
            p1_k = 24
            p2_k = 16
        elif p1_rating < 2100:
            p1_k = 32
            p2_k = 16
    
    # Calculate players' ELO ratings
    if p1_wins_bool == True:
        p1_rating = p1_rating + p1_k * (1 - p1_probability)
        p2_rating = p2_rating + p2_k * (0 - p2_probability)
    else:
        p1_rating = p1_rating + p1_k * (0 - p1_probability)
        p2_rating = p2_rating + p2_k * (1 - p2_probability)
    
    # Set new ratings to Player objects
    p1.set_rating(p1_rating)
    p2.set_rating(p2_rating)
    