from event import GameEvent
from notification import NotificationService
from position_tracker import PositionTracker
from scoreboard import Scoreboard


class Game(NotificationService):
    def __init__(self, team1, team2, runs_to_win, wickets_left, overs_left):
        super().__init__()
        self.scoreboard = Scoreboard(team1, team2, runs_to_win, wickets_left, overs_left)
        self.position_tracker = PositionTracker(team1, team2)
        self.scoreboard.add_observers([self])

    def notify(self, event):
        self.position_tracker = self.position_tracker.notify(event)

    def notify_winner(self, win_event):
        self.winner = win_event

    def add_observers(self, observers):
        self.scoreboard.add_observers(observers)

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
