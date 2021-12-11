class Player:
    def __init__(self, id, rating=1000, win_count=0, lose_count=0, win_streak=0, best_win_streak=0):
        self.id = id
        self.rating = rating
        self.win_count = win_count
        self.lose_count = lose_count
        self.win_streak = win_streak
        self.best_win_streak = best_win_streak

    def get_player(self, id):
        if id == self.id:
            return self
        else:
            print("Player not found.")

    def get_rating(self):
        return self.rating

    def set_rating(self, rating):
        self.rating = rating

    def plus_win(self):
        self.win_count += 1
        self.win_streak += 1
        if self.win_streak > self.best_win_streak:
            self.best_win_streak = self.win_streak

    def plus_lose(self):
        self.lose_count += 1
        self.win_streak = 0