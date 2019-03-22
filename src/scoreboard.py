from constants import number_of_balls_in_over, draw_message
from event import NotificationEvent, WinEvent
from notification import NotificationService
from observer import Observer
from team import Team
from umpire import is_batter_out

from player_statistics import PlayerStatsService


class Scoreboard(Observer):
    def __init__(self, batting_team, bowling_team, wickets_left, overs_left, innings, runs_to_win=-1):
        super().__init__()
        self.innings = innings
        self.balls_left = overs_left * number_of_balls_in_over
        self.wickets_left = wickets_left
        self.runs_to_win = runs_to_win
        self.bowling_team = bowling_team
        self.batting_team = batting_team
        self.player_statistics_service = PlayerStatsService(batting_team)
        self.notification_service = NotificationService()
        self.runs_scored = 0
        self.balls_played = 0

    def update_runs_to_win(self, runs_to_win):
        self.runs_to_win = runs_to_win
        self.innings = 2
        return self

    def add_observers(self, observers):
        self.notification_service.add_observers(observers)

    def __str__(self):
        return "Scoreboard " + str(self.balls_left) + "," + str(self.wickets_left) + "," + str(
            self.runs_to_win) + "," + str(self.player_statistics_service)

    def update_runs(self, runs):
        if self.innings == 2:
            self.runs_to_win = self.runs_to_win - runs
        self.runs_scored = self.runs_scored + runs

    def update_score(self, game_event):
        batter = game_event.batter
        is_out = is_batter_out(game_event.outcome)
        runs = 0 if is_out else int(game_event.outcome)
        if is_out:
            self.wickets_left = self.wickets_left - 1
        else:
            self.update_runs(runs)
        self.balls_left = self.balls_left - 1
        self.player_statistics_service = self.player_statistics_service.add_statistic(batter, runs, is_out)
        self.balls_played = game_event.balls_played
        return batter, is_out, runs

    def notify(self, game_event):
        batter, is_out, runs = self.update_score(game_event)

        notification_service = self.notification_service
        notification_service.notify(
            NotificationEvent(self.balls_played, batter, runs, is_out,
                              self.balls_left, self.runs_to_win, self.wickets_left,
                              self.player_statistics_service.player_statistics[batter.name])
        )
        if self.innings == 2:
            if self.runs_to_win <= 0:
                notification_service.notify_winner(
                    WinEvent(self.batting_team, self.wickets_left, self.balls_left, self.runs_to_win))
            elif self.runs_to_win == 1 and self.balls_left == 0:
                notification_service.notify_winner(
                    WinEvent(Team(draw_message, []), self.wickets_left, self.balls_left, self.runs_to_win))
        if self.wickets_left == 0 or self.balls_left == 0:
            notification_service.notify_winner(
                WinEvent(self.bowling_team, self.wickets_left, self.balls_left, self.runs_to_win))

    def summary(self):
        return self.batting_team, self.runs_scored
