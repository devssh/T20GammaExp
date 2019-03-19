from event import GameEvent
from notification import NotificationService
from scoreboard import Scoreboard


class Game(NotificationService):
    def __init__(self, team1, team2, runs_to_win, wickets_left, overs_left):
        super().__init__()
        self.batters = team1
        self.bowlers = team2
        self.scoreboard = Scoreboard(team1, team2, runs_to_win, wickets_left, overs_left)
        self.balls_played = 0
        self.current_batsman = 0
        self.scoreboard.add_observers([self, team1, team2])

    def notify_winner(self, win_event):
        self.winner = win_event

    def add_observers(self, observers):
        self.scoreboard.add_observers(observers)

    def switch_current_batsman(self):
        self.current_batsman = (self.current_batsman + 1) % 2

    def select_current_batsman(self):
        if self.current_batsman == 0:
            return self.batters.select_first_batsman()
        return self.batters.select_second_batsman()

    def increase_balls_played(self):
        self.balls_played = self.balls_played + 1

    def is_new_over(self):
        if self.balls_played % 6 == 0:
            return True
        return False

    def notify(self, event):
        if not event.is_out:
            if event.runs % 2 == 1:
                self.switch_current_batsman()

    def play_ball(self):
        self.increase_balls_played()
        current_batsman = self.select_current_batsman()
        outcome = current_batsman.bat()
        self.scoreboard.notify(GameEvent(self.balls_played, current_batsman, outcome))
        if self.is_new_over():
            self.switch_current_batsman()
        return outcome

    def play(self):
        while not self.winner:
            self.play_ball()
