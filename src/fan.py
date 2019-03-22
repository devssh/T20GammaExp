from collections import OrderedDict

from observer import Observer
from player_statistics import PlayerStatistic


class Fan(Observer):
    def __init__(self, supports_team):
        super().__init__()
        self.supports_team = supports_team
        self.stats = OrderedDict()

    def notify(self, event):
        for player in event.batting_team.players:
            if player.name not in self.stats:
                self.stats[player.name] = PlayerStatistic(player)
        stats = event.batter_statistics
        self.stats[stats.player.name] = stats

    def summarize_match(self):
        stats = self.stats
        summary = str(self.winner) + "\n\n" + "\n".join(
            [str(stats[player_name]) for player_name in stats]) + "\n\n"
        return summary
