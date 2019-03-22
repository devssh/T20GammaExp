from event import GameEvent
from notification import NotificationService
from scoreboard import Scoreboard

from position_tracker import PositionTracker


class Inning(NotificationService):
    def __init__(self, batters, bowlers, wickets_left, overs_left, number=1):
        super().__init__()
        self.scoreboard = Scoreboard(batters, bowlers, wickets_left, overs_left, number)
        self.position_tracker = PositionTracker(batters, bowlers)
        self.scoreboard.add_observers([self])

    def update_runs_to_win(self, runs_to_win):
        self.scoreboard = self.scoreboard.update_runs_to_win(runs_to_win)
        return self

    def notify(self, event):
        self.position_tracker = self.position_tracker.notify(event)

    def notify_winner(self, win_event):
        self.winner = win_event

    def add_observers(self, observers):
        self.scoreboard.add_observers(observers)
        return self

    def select_current_batsman(self):
        return self.position_tracker.select_current_batsman()

    def play_ball(self):
        current_batsman = self.select_current_batsman()
        outcome = current_batsman.bat()
        tracker = self.position_tracker
        self.scoreboard.notify(GameEvent(tracker.balls_played, current_batsman, outcome))
        return outcome

    def play(self):
        while not self.winner:
            self.play_ball()
        return self.scoreboard.summary()
