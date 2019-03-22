from constants import number_of_balls_in_over
from observer import Observer


def display_over_count(balls_played):
    over_number = int((balls_played - 1) / number_of_balls_in_over)
    over_fraction = round((((balls_played - 1) % number_of_balls_in_over) / 10) + 0.1, 1)
    return str(round(over_number + over_fraction, 1))


def excited_commentary(event):
    runs = event.runs
    batter_name = event.batter.name
    is_out = event.is_out
    balls_played = event.balls_played
    wickets_left = event.wickets_left
    batting_team = event.batting_team
    if is_out:
        out_message = display_over_count(balls_played) + " " + batter_name + " gets out! " + (
        "" if wickets_left > 0 else batting_team.name + " all out!")
        return out_message
    return display_over_count(balls_played) + " " + batter_name + " scores " + str(runs) + (
        " run" if runs == 1 else " runs" if runs < 4 else " runs!")


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


class ExcitedCommentator(Observer):
    def commentary(self):
        events = self.events
        teams = list(set([event.batting_team.name for event in events]))
        if events[0].batting_team.name != teams[0]:
            teams = list(reversed(teams))
        commentary = ""
        for team in teams:
            commentary = commentary + "\n"
            team_events = [event for event in events if event.batting_team.name == team]
            commentary = commentary + team + " innings:\n"
            for event in team_events:
                commentary = commentary + excited_commentary(event) + "\n"
        return commentary[:-1] + " " + str(self.winner.winning_team.name) + " wins!"
