
is_out = "is_out"
not_out = "not_out"


class Umpire:
    def __init__(self, runs_to_win, wickets_left):
        self.runs_to_win = runs_to_win
        self.wickets_left = wickets_left

    def decides_is_out(self, outcome):
        if outcome == is_out:
            self.wickets_left = self.wickets_left - 1
            return True
        return False

    def decide_winner(self, team1, team2, runs):
        if (self.runs_to_win - runs < 0) and (self.wickets_left > 0):
            return team1
        elif self.wickets_left == 0:
            return team2
        elif self.runs_to_win - runs == 0:
            return "Draw"

