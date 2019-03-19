from constants import number_of_balls_in_over, number_of_batters
from observer import Observer


class PositionTracker(Observer):
    def __init__(self, batters, bowlers):
        super().__init__()
        self.bowlers = bowlers
        self.batters = batters
        self.current_batsman = 0
        self.balls_played = 0
        if len(batters.players) < 2:
            raise ValueError("Cannot select batsmen, team does not have enough batters")
        self.available_batters = batters.players

    def select_first_batsman(self):
        if len(self.available_batters) < 2:
            raise ValueError("Cannot select batsmen, team is out")
        return self.available_batters[0]

    def select_second_batsman(self):
        if len(self.available_batters) < number_of_batters:
            raise ValueError("Cannot select second batsmen, team is out")
        return self.available_batters[1]

    def switch_current_batsman(self):
        self.current_batsman = (self.current_batsman + 1) % number_of_batters

    def is_new_over(self):
        if self.balls_played % number_of_balls_in_over == 0:
            return True
        return False

    def increase_balls_played(self):
        self.balls_played = self.balls_played + 1

    def select_current_batsman(self):
        self.increase_balls_played()
        if self.current_batsman == 0:
            return self.select_first_batsman()
        return self.select_second_batsman()

    def notify(self, event):
        batter = event.batter
        if event.is_out:
            self.available_batters = [player for player in self.available_batters if
                                      player.name != batter.name]
        else:
            if event.runs % 2 == 1:
                self.switch_current_batsman()

        if self.is_new_over():
            self.switch_current_batsman()
        return self
