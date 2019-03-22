import sys

from team import Team
from umpire import toss_coin_to_decide_who_bats_first

if __name__ == '__main__':
    weather = str(sys.argv[1]).lower()
    time = str(sys.argv[2]).lower()

    team1 = Team("Lengaburu", [], True, True)
    team2 = Team("Enchai", [], False, False)
    toss_outcome, team_decision, batter, bowler = toss_coin_to_decide_who_bats_first(team1, team2, weather, time)

    if toss_outcome:
        print("Lengaburu wins the toss. They decide to " + ("bat" if team_decision else "bowl"))
    else:
        print("Enchai wins the toss. They decide to " + ("bat" if team_decision else "bowl"))
