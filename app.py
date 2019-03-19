from commentator import Commentator
from fan import Fan
from game import Game
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
    game = Game(team_bangalore, team_chennai, runs_to_win, wickets_left, overs_left)

    fan = Fan(team_bangalore)
    commentator = Commentator()
    observers = [fan, commentator]
    game.add_observers(observers)
    winner = game.play()
    print(fan.summarize_match())
    print(commentator.commentary())
