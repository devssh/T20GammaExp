from team import Team
from game import number_of_balls_in_over

is_out = "is_out"
not_out = "not_out"


class Umpire:
    def __init__(self, runs_to_win, wickets_left, overs_left):
        self.runs_to_win = runs_to_win
        self.wickets_left = wickets_left
        self.overs_to_win = overs_left
        self.balls_played = 0

    def decides_is_out(self, outcome):
        self.balls_played = self.balls_played + 1
        if outcome == is_out:
            self.wickets_left = self.wickets_left - 1
            return True
        return False

    def decide_winner(self, team1, team2, runs):
        if (self.runs_to_win - runs < 0) and (self.wickets_left > 0):
            return team1
        elif self.wickets_left == 0:
            return team2
        elif self.runs_to_win - runs == 0 and int(self.balls_played / number_of_balls_in_over) == self.overs_to_win:
            return Team("Draw", [], 0)
        else:
            if not self.is_game_over(runs):
                raise ValueError("Match is not over yet")
            else:
                raise ValueError("Error in deciding winner")

    def is_game_over(self, runs):
        if (self.wickets_left == 0) or (self.runs_to_win - runs < 0) or (int(
                        self.balls_played / number_of_balls_in_over) == self.overs_to_win):
            return True
        return False
