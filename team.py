from observer import Observer


class Team(Observer):
    def __init__(self, name, players):
        super().__init__()
        self.players = players
        self.available_players = players
        self.name = name

    def select_first_batsman(self):
        if len(self.available_players) < 2:
            raise ValueError("Cannot select batsmen, team is out")
        return self.available_players[0]

    def select_second_batsman(self):
        if len(self.available_players) < 2:
            raise ValueError("Cannot select second batsmen, team is out")
        return self.available_players[1]

    def notify(self, notification_event):
        is_out = notification_event.is_out
        batter = notification_event.batter
        if is_out:
            self.available_players = [player for player in self.available_players if
                                      player.name != batter.name]

    def __str__(self):
        return self.name + ": " + str(self.players)

    def __repr__(self):
        return self.__str__()
