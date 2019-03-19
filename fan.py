from collections import OrderedDict

from observer import Observer


class Fan(Observer):
    def __init__(self, supports_team):
        super().__init__()
        self.supports_team = supports_team

    def summarize_match(self):
        statistics = OrderedDict([(event.batter.name, event.batter_statistics) for event in self.events])
        summary = str(self.winner) + "\n\n" + "\n".join(
            [str(statistics[player_name]) for player_name in statistics]) + "\n\n"
        return summary
