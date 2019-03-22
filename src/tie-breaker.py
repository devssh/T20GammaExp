from commentator import ExcitedCommentator
from fan import Fan
from game import Cricket
from player import Player

from team import Team

if __name__ == '__main__':
    overs_left = 1

    team_bangalore = Team("Lengaburu", [
        Player('Kirat Boli', [0.05, 0.1, 0.25, 0.1, 0.25, 0.01, 0.14, 0.10]),
        Player('N.S Nodhi', [0.05, 0.15, 0.15, 0.1, 0.2, 0.01, 0.19, 0.15]),
    ])

    team_chennai = Team("Enchai", [
        Player('DB Vellyers', [0.05, 0.1, 0.25, 0.1, 0.25, 0.01, 0.14, 0.10]),
        Player('H Mamla', [0.05, 0.15, 0.15, 0.1, 0.2, 0.01, 0.19, 0.15]),
    ])
    # h mamla has pdf > 1 in the geektrust website!

    game = Cricket(team_bangalore, team_chennai, overs_left)

    fan = Fan(team_bangalore)
    commentator = ExcitedCommentator()
    observers = [fan, commentator]
    game.add_observers(observers)
    game.play()
    print(fan.summarize_match())
    print(commentator.commentary())
