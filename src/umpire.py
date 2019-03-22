from randomizer import flip_coin, HEADS

out = "out"
not_out = "not_out"


def is_batter_out(outcome):
    if outcome == out:
        return True
    return False


def toss_coin_to_decide_who_bats_first(team1, team2, weather, time):
    toss_outcome = flip_coin() == HEADS
    winner = team1 if toss_outcome else team2
    loser = team1 if toss_outcome else team2
    team_decision = winner.decide_to_bat(weather, time)
    batter = winner if team_decision else loser
    bowler = loser if team_decision else winner
    return toss_outcome, team_decision, batter, bowler
