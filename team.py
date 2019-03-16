class Team:
    def __init__(self, name, players, wickets_left):
        self.players = players
        self.name = name
        self.wickets_left = wickets_left

    def select_batters(self):
        return self.players[-self.wickets_left - 1: -self.wickets_left + 1]

    def next_batter(self):
        self.wickets_left = self.wickets_left - 1
        return self.players[-self.wickets_left]

