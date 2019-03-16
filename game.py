overs_left = 4
runs_to_win = 40
wickets_left = 3
number_of_balls_in_over = 6


class Game:
    def __init__(self, team1, team2, umpire, overs_left):
        self.team1 = team1
        self.team2 = team2
        self.umpire = umpire
        self.batters = team1.select_batters()
        self.observers = []
        self.runs = 0
        self.overs = 0
        self.overs_left = overs_left

    def add_observers(self, observers):
        self.observers = self.observers.append(*observers)

    def is_game_over(self, wickets_left, runs_left):
        if wickets_left == 0 or runs_left <= 0:
            return True
        return False

    def notify_observers_score(self, batter, runs):
        [observer.notify_score(batter, runs) for observer in self.observers]

    def notify_observers_winner(self, winner):
        [observer.notify_winner(winner) for observer in self.observers]

    def switch_batters(self):
        self.batters = reversed(self.batters)

    def increment_runs(self, runs):
        self.runs = self.runs + runs

    def increment_over_count(self):
        if self.overs % 1 == 0.6:
            return int(self.overs) + 1
        else:
            return self.overs + 0.1

    def play(self):

        while ~self.is_game_over(self.wickets_left, self.runs_to_win - self.runs):
            outcome, runs = self.batters[0].bat()
            self.overs = self.increment_over_count()
            if self.umpire.decides_is_out(outcome):
                self.batters = [self.team1.next_batter(), self.batters[1]]
                self.wickets_left = self.wickets_left - 1
            else:
                self.increment_runs(runs)
                self.notify_observers_score(self.batters[0], runs)
                if runs % 2 == 1:
                    self.switch_batters()

        winner = umpire.decide_winner(self.runs)
        self.notify_observers_winner(winner)
        return winner

