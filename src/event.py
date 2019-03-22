from commentator import display_over_count
from constants import draw_message


class NotificationEvent:
    def __init__(self, balls_played, batter, runs, is_out, balls_left, runs_to_win, wickets_left, batter_statistics,
                 batting_team):
        self.batting_team = batting_team
        self.balls_left = balls_left
        self.batter_statistics = batter_statistics
        self.wickets_left = wickets_left
        self.runs_to_win = runs_to_win
        self.is_out = is_out
        self.runs = runs
        self.batter = batter
        self.balls_played = balls_played

    def __str__(self):
        runs = self.runs
        batter_name = self.batter.name
        is_out = self.is_out
        balls_played = self.balls_played
        if is_out:
            out_message = display_over_count(balls_played) + " " + batter_name + " gets out!"
            return out_message
        return display_over_count(balls_played) + " " + batter_name + " scores " + str(runs) + (
            " run" if runs == 1 else " runs")

    def show(self):
        return "Notification event " + str(self.balls_left) + "," + str(self.batter_statistics) + "," + str(
            self.wickets_left) + "," + str(self.runs_to_win) + "," + str(self.is_out) + "," + str(
            self.runs) + "," + str(
            self.batter) + "," + str(self.balls_played)


class GameEvent:
    def __init__(self, balls_played, batter, outcome):
        self.outcome = outcome
        self.batter = batter
        self.balls_played = balls_played

    def __str__(self):
        return "GameEvent " + str(self.batter) + "," + self.outcome + "," + str(self.balls_played)


class WinEvent:
    def __init__(self, winning_team, wickets_remaining, balls_remaining, runs_remaining):
        self.winning_team = winning_team
        self.runs_remaining = runs_remaining
        self.balls_remaining = balls_remaining
        self.wickets_remaining = wickets_remaining

    def __str__(self):
        winner_name = self.winning_team.name
        wickets_remaining = self.wickets_remaining
        balls_remaining = self.balls_remaining
        runs_remaining = self.runs_remaining

        balls_string = " balls" if balls_remaining > 1 or balls_remaining == 0 else " ball"
        if winner_name == draw_message:
            return "\nThe match ended in a draw"
        elif wickets_remaining > 0 and balls_remaining >= 0 and runs_remaining <= 0:
            return "\n" + winner_name + " won by " + str(wickets_remaining) + (
                " wickets" if wickets_remaining > 1 else " wicket") + " and " + str(
                balls_remaining
            ) + balls_string + " remaining"
        return "\n" + winner_name + " won by " + str(runs_remaining) + (
            " runs" if runs_remaining > 1 else " run") + " and " + str(
            balls_remaining
        ) + balls_string + " remaining"
