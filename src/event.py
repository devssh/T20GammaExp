from constants import number_of_balls_in_over, draw_message


class NotificationEvent:
    def __init__(self, balls_played, batter, runs, is_out, balls_left, runs_to_win, wickets_left, batter_statistics):
        self.balls_left = balls_left
        self.batter_statistics = batter_statistics
        self.wickets_left = wickets_left
        self.runs_to_win = runs_to_win
        self.is_out = is_out
        self.runs = runs
        self.batter = batter
        self.balls_played = balls_played

    def display_over_count(self):
        over_number = int((self.balls_played - 1) / number_of_balls_in_over)
        over_fraction = round((((self.balls_played - 1) % number_of_balls_in_over) / 10) + 0.1, 1)
        return str(round(over_number + over_fraction, 1))

    def __str__(self):
        runs = self.runs
        batter_name = self.batter.name
        if self.is_out:
            out_message = self.display_over_count() + " " + batter_name + " gets out!"
            return out_message
        return self.display_over_count() + " " + batter_name + " scores " + str(runs) + (
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
        if self.wickets_remaining > 0 and self.balls_remaining >= 0 and self.runs_remaining < 0:
            return "\n" + self.winning_team.name + " won by " + str(self.wickets_remaining) + " wickets and " + str(
                self.balls_remaining
            ) + " balls remaining"
        elif self.winning_team.name == draw_message:
            return "\nThe match ended in a draw"
        return "\n" + self.winning_team.name + " won by " + str(self.runs_remaining) + " runs and " + str(
            self.balls_remaining
        ) + " balls remaining"
