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
        self.observers = [*self.observers, *observers]

    def notify_observers_score(self, over_count, batter, runs):
        [observer.notify_score(over_count, batter, runs) for observer in self.observers]

    def notify_observers_out(self, over_count, batter):
        [observer.notify_out(over_count, batter) for observer in self.observers]

    def notify_observers_winner(self, winner):
        [observer.notify_winner(winner) for observer in self.observers]

    def switch_batters(self):
        return list(reversed(self.batters))

    def increment_runs(self, runs):
        return self.runs + runs

    def increment_over_count(self):
        if round(self.overs % 1, 1) == 0.6:
            return round(int(self.overs) + 1.1, 1)
        else:
            return round(self.overs + 0.1, 1)

    def is_new_over(self):
        if self.overs % 1 == 0.6:
            return True
        return False

    def get_current_batsman(self):
        return self.batters[0]

    def play(self):
        while not self.umpire.is_game_over(self.runs):
            if self.is_new_over():
                self.batters = self.switch_batters()
            self.overs = self.increment_over_count()
            current_batsman = self.get_current_batsman()
            out_status, runs = current_batsman.bat()
            if self.umpire.decides_is_out(out_status):
                self.batters = [self.team1.next_batter(), self.batters[1]]
                self.notify_observers_out(self.overs, current_batsman)
            else:
                self.runs = self.increment_runs(runs)
                self.notify_observers_score(self.overs, current_batsman, runs)
                if runs % 2 == 1:
                    self.batters = self.switch_batters()
        winner = self.umpire.decide_winner(self.team1, self.team2, self.runs)
        self.notify_observers_winner(winner)
        return winner
