class Team:
    def __init__(self, name, players):
        super().__init__()
        self.players = players
        self.available_players = players
        self.name = name

    def __str__(self):
        return self.name + ": " + str(self.players)

    def __repr__(self):
        return self.__str__()
