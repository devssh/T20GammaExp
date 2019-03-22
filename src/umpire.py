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
    loser = team2 if toss_outcome else team1
    is_batting = winner.decide_to_bat(weather, time)
    batter = winner if is_batting else loser
    bowler = loser if is_batting else winner
    return toss_outcome, is_batting, batter, bowler
