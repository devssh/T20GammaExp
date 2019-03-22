from commentator import Commentator
from fan import Fan
from innings import Inning
from player import Player

from team import Team

if __name__ == '__main__':
    overs_left = 4
    runs_to_win = 40
    wickets_left = 3

    team_bangalore = Team("Lengaburu", [
        Player('Kirat Boli', [0.05, 0.3, 0.25, 0.1, 0.15, 0.01, 0.09, 0.05]),
        Player('N.S Nodhi', [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.04, 0.1]),
        Player('R Rumrah', [0.2, 0.3, 0.15, 0.05, 0.05, 0.01, 0.04, 0.2]),
        Player('Shashi Henra', [0.3, 0.25, 0.05, 0, 0.05, 0.01, 0.04, 0.3])
    ])

    team_chennai = Team("Enchai", [])
    inning2 = Inning(team_bangalore, team_chennai, wickets_left, overs_left, number=2).update_runs_to_win(runs_to_win)

    fan = Fan(team_bangalore)
    commentator = Commentator()
    observers = [fan, commentator]
    inning2.add_observers(observers)
    winner = inning2.play()
    print(fan.summarize_match())
    print(commentator.commentary())
