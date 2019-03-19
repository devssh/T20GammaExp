from event import NotificationEvent, WinEvent
from constants import number_of_balls_in_over, draw_message
from notification import NotificationService
from observer import Observer
from player_statistics import PlayerStatsService
from team import Team
from umpire import is_batter_out


class Scoreboard(Observer):
    def __init__(self, batting_team, bowling_team, runs_to_win, wickets_left, overs_left):
        super().__init__()
        self.balls_left = overs_left * number_of_balls_in_over
        self.wickets_left = wickets_left
        self.runs_to_win = runs_to_win
        self.bowling_team = bowling_team
        self.batting_team = batting_team
        self.player_statistics_service = PlayerStatsService(batting_team)
        self.notification_service = NotificationService()

    def add_observers(self, observers):
        self.notification_service.add_observers(observers)

    def __str__(self):
        return "Scoreboard " + str(self.balls_left) + "," + str(self.wickets_left) + "," + str(
            self.runs_to_win) + "," + str(self.player_statistics_service)

    def notify(self, game_event):
        batter = game_event.batter
        is_out = is_batter_out(game_event.outcome)
        runs = 0 if is_out else int(game_event.outcome)
        if is_out:
            self.wickets_left = self.wickets_left - 1
        else:
            self.runs_to_win = self.runs_to_win - runs
        self.balls_left = self.balls_left - 1
        self.player_statistics_service = self.player_statistics_service.add_statistic(batter, runs, is_out)

        notification_service = self.notification_service
        notification_service.notify(
            NotificationEvent(game_event.balls_played, batter, runs, is_out,
                              self.balls_left, self.runs_to_win, self.wickets_left,
                              self.player_statistics_service.player_statistics[batter.name])
        )
        if self.runs_to_win <= 0:
            notification_service.notify_winner(
                WinEvent(self.batting_team, self.wickets_left, self.balls_left, self.runs_to_win))
        elif self.wickets_left == 0 or self.balls_left == 0:
            notification_service.notify_winner(
                WinEvent(self.bowling_team, self.wickets_left, self.balls_left, self.runs_to_win))
        elif self.runs_to_win == 1 and self.balls_left == 0:
            notification_service.notify_winner(
                WinEvent(Team(draw_message, []), self.wickets_left, self.balls_left, self.runs_to_win))
