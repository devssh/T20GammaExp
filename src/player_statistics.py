from collections import OrderedDict


class PlayerStatistic:
    def __init__(self, player):
        self.player = player
        self.is_out = False
        self.balls_played = 0
        self.runs = 0

    def add_statistic(self, runs, is_out):
        if is_out:
            self.is_out = True
        else:
            self.runs = self.runs + runs
        self.balls_played = self.balls_played + 1
        return self

    def __str__(self):
        player_name = self.player.name
        return player_name + " - " + str(self.runs) + (
            "" if self.is_out else "*"
        ) + " (" + str(self.balls_played) + " balls)"

    def __repr__(self):
        return self.__str__()


class PlayerStatsService:
    def __init__(self, team):
        self.team = team
        self.player_statistics = OrderedDict([(player.name, PlayerStatistic(player)) for player in team.players])

    def add_statistic(self, player, runs, is_out):
        self.player_statistics[player.name] = self.player_statistics[player.name].add_statistic(runs, is_out)
        return self
