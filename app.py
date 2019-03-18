from team import Team
from player import Player
from umpire import Umpire
from game import Game
from observers import Fan
from observers import Commentator

if __name__ == '__main__':
    overs_left = 4
    runs_to_win = 40
    wickets_left = 3

    team_bangalore = Team("Bengaluru", [
        Player('Kirat Boli', 24, 0.05), Player('NS Nodhi', 10, 0.5), Player('R Rumrah', 9),
        Player('Shashi Henra', 6)
    ], wickets_left)

    team_chennai = Team("Chennai", [], 0)
    umpire = Umpire(runs_to_win, wickets_left, overs_left)
    game = Game(team_bangalore, team_chennai, umpire, overs_left)

    fan = Fan(team_bangalore, overs_left, runs_to_win, wickets_left)
    commentator = Commentator(overs_left, runs_to_win, wickets_left)
    observers = [fan, commentator]
    game.add_observers(observers)
    winner = game.play()
    print(fan.summarize_match())
    print(commentator.commentary())
