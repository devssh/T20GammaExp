from innings import Inning
from randomizer import flip_coin, HEADS

from notification import NotificationService


class Cricket(NotificationService):
    def __init__(self, team1, team2, total_overs):
        super().__init__()
        self.total_overs = total_overs
        self.team2 = team2
        self.team1 = team1
        self.coin_toss_outcome = False
        self.inning1 = False
        self.inning2 = False
        self.inning1_summary = False
        self.inning2_summary = False

    def play(self):
        self.coin_toss_outcome = flip_coin()
        if self.coin_toss_outcome == HEADS:
            self.inning1 = Inning(self.team1, self.team2, len(self.team1.players), self.total_overs, number=1)
            self.inning2 = Inning(self.team2, self.team1, len(self.team1.players), self.total_overs, number=2)
        else:
            self.inning1 = Inning(self.team2, self.team1, len(self.team1.players), self.total_overs, number=1)
            self.inning2 = Inning(self.team1, self.team2, len(self.team1.players), self.total_overs, number=2)
        self.inning1 = self.inning1.add_observers([*self.observers, self])
        self.inning1_summary = self.inning1.play()
        self.inning2 = self.inning2.update_runs_to_win(self.inning1_summary[1]).add_observers([*self.observers, self])
        self.inning2_summary = self.inning2.play()
        return self.winner
