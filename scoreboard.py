from event import NotificationEvent, WinEvent
from constants import number_of_balls_in_over, draw_message
from notification import NotificationService
from player_statistics import PlayerStatsService
from team import Team
from umpire import is_batter_out


class Scoreboard(NotificationService):
    def __init__(self, batting_team, bowling_team, runs_to_win, wickets_left, overs_left):
        super().__init__()
        self.balls_left = overs_left * number_of_balls_in_over
        self.wickets_left = wickets_left
        self.runs_to_win = runs_to_win
        self.bowling_team = bowling_team
        self.batting_team = batting_team
        self.player_statistics_service = PlayerStatsService(batting_team)

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

        for observer in self.observers:
            observer.notify(
                NotificationEvent(game_event.balls_played, batter, runs, is_out,
                                  self.balls_left, self.runs_to_win, self.wickets_left,
                                  self.player_statistics_service.player_statistics[batter.name])
            )
            if self.runs_to_win <= 0:
                observer.notify_winner(
                    WinEvent(self.batting_team, self.wickets_left, self.balls_left, self.runs_to_win))
            elif self.wickets_left == 0 or self.balls_left == 0:
                observer.notify_winner(
                    WinEvent(self.bowling_team, self.wickets_left, self.balls_left, self.runs_to_win))
            elif self.runs_to_win == 1 and self.balls_left == 0:
                observer.notify_winner(
                    WinEvent(Team(draw_message, []), self.wickets_left, self.balls_left, self.runs_to_win))
