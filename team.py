class Team:
    def __init__(self, name, players, wickets_left, has_finished_batting = False):
        self.players = players
        self.name = name
        if wickets_left < 1 and not has_finished_batting:
            raise ValueError("Invalid number of wickets left")
        self.wickets_left = wickets_left

    def select_batters(self):
        return self.players[-self.wickets_left - 1: -self.wickets_left + 1]

    def next_batter(self):
        self.wickets_left = self.wickets_left - 1
        return self.players[-self.wickets_left]

    def __str__(self):
        return self.name + ": " + str(self.players)

    def __repr__(self):
        return self.__str__()
