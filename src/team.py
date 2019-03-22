CLOUDY = "cloudy"
CLEAR = "clear"
DAY = "day"
NIGHT = "night"


class Team:
    def __init__(self, name, players, weather_preferences=False, time_preferences=False):
        super().__init__()
        self.time_preferences = time_preferences
        self.weather_preferences = weather_preferences
        self.players = players
        self.available_players = players
        self.name = name

    def __str__(self):
        return self.name + ": " + str(self.players)

    def __repr__(self):
        return self.__str__()

    def decide_to_bat(self, weather, time):
        current_weather = weather == "clear"
        current_time = time == "day"
        if (current_weather == self.weather_preferences) or (current_time == self.time_preferences):
            return True
        return False
