from observer import Observer

from constants import number_of_balls_in_over


class Commentator(Observer):
    def commentary(self):
        commentary = ""
        for event in self.events:
            if event.balls_left % number_of_balls_in_over == 5:
                commentary = commentary + "\n" + str(
                    int((event.balls_left + 1) / number_of_balls_in_over)) + " overs left. " + str(
                    event.runs_to_win + event.runs) + " runs to win\n\n"
            commentary = commentary + str(event) + "\n"
        return commentary + str(self.winner)


class Commentator2(Observer):
    def commentary(self):
        events = self.events
        teams = list(set([event.batting_team.name for event in events]))
        if events[0].batting_team.name != teams[0]:
            teams = list(reversed(teams))
        commentary = ""
        for team in teams:
            team_events = [event for event in self.events if event.batting_team.name == team]
            commentary = commentary + team + " innings:\n"
            for event in team_events:
                commentary = commentary + str(event) + "\n"
        return commentary + str(self.winner)
