from constants import number_of_balls_in_over
from observer import Observer


class Commentator(Observer):
    def commentary(self):
        commentary = ""
        for event in self.events:
            if event.balls_left % number_of_balls_in_over == 5:
                commentary = commentary + "\n" + str(
                    int((event.balls_left + 1) / number_of_balls_in_over)) + " overs left. " + str(
                    event.runs_to_win + event.runs) + " runs to win\n"
            commentary = commentary + str(event) + "\n"
        return commentary + str(self.winner)
