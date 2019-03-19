import traceback

from player import Player
from team import Team
from umpire import Umpire, out, not_out
from observers import Commentator, Fan
from game import Game

pass_count = 0
total_test_count = 54


def test_passed():
    global pass_count
    pass_count = pass_count + 1
    print(pass_count, "/", total_test_count)


def test_failed():
    print_assert_error("Expecting ValueError to be raised", False)


def print_assert_error(error_msg, predicate):
    try:
        assert predicate
        test_passed()
    except AssertionError:
        print(error_msg + "\n" + str(traceback.format_exc()))


def assert_true(error_msg, predicate):
    print_assert_error(error_msg, predicate)


def assert_exception(some_func):
    try:
        some_func(0)
        test_failed()
    except ValueError:
        assert True
        test_passed()


def test_player_raises_exception_on_invalid_input():
    assert_exception(lambda x: Player("x", [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.4, 0.5]))


def test_team_assigns_batters_correctly():
    players = [Player("x", [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.04, 0.1]),
               Player("y", [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.04, 0.1]),
               Player("z", [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.04, 0.1]),
               Player("a", [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.04, 0.1])]
    some_team = Team("xyz", players, 3)
    batters = some_team.select_batters()
    next_batter = some_team.next_batter()
    assert_true("invalid batters selected", batters[0] == players[0])
    assert_true("invalid batters selected", batters[1] == players[1])
    assert_true("invalid next batter selected", next_batter == players[2])
    assert_exception(lambda x: Team("xyz", [], 0))


def test_umpire_decides_correctly():
    umpire = Umpire(runs_to_win=10, wickets_left=3, overs_left=5)
    assert_true("umpire ends game early", not umpire.is_game_over(runs=1))
    assert_true("umpire ends game on draw", not umpire.is_game_over(runs=10))
    assert_true("umpire doesn't end game correcly", umpire.is_game_over(runs=11))
    assert_true("umpire decides out fairly", umpire.decides_is_out(outcome=out))
    assert_true("umpire not out happy path", not umpire.decides_is_out(outcome=not_out))
    umpire.decides_is_out(outcome=out)
    umpire.decides_is_out(outcome=out)
    assert_true("umpire ends game on wickets over", umpire.is_game_over(runs=7))

    team1 = Team("y", [Player("x", 7), Player("y", 7), Player("z", 7), Player("a", 7)], 3)
    team2 = Team("x", [], 1)
    assert_true("umpire decides winner happy path for losing wickets out",
                umpire.decide_winner(team1, team2, 9).name == team2.name)
    umpire = Umpire(runs_to_win=10, wickets_left=3, overs_left=5)
    assert_true("umpire decides winner happy path", umpire.decide_winner(team1, team2, 14).name == team1.name)


def test_observers_store_memories():
    commentator = Commentator(5, 100, 3)
    commentator.notify_out(0.1, Player("x", 7))
    commentator.notify_score(0.1, Player("x", 7), 10)
    commentator.notify_score(0.1, Player("y", 7), 10)
    assert_true("commentator not storing memories correctly", len(commentator.memories) == 3)

    fan = Fan("xyz", 5, 100, 3)
    fan.notify_out(0.1, Player("x", 7))
    fan.notify_score(0.1, Player("x", 7), 10)
    fan.notify_score(0.1, Player("y", 7), 10)
    assert_true("fan not storing memories correctly", len(fan.memory) == 2)


def test_game_plays_correctly_integration_test():
    overs_left = 20
    runs_to_win = 400
    wickets_left = 3

    team_bangalore = Team("Bengaluru", [
        Player('Kirat Boli', 26, 0.0001), Player('NS Nodhi', 10, 0.0001), Player('R Rumrah', 9, 0.0001),
        Player('Shashi Henra', 6)
    ], wickets_left)

    team_chennai = Team("Chennai", [], 0, has_finished_batting=True)
    umpire = Umpire(runs_to_win, wickets_left, overs_left)
    game = Game(team_bangalore, team_chennai, umpire, overs_left)

    fan = Fan(team_bangalore, overs_left, runs_to_win, wickets_left)
    commentator = Commentator(overs_left, runs_to_win, wickets_left)
    observers = [fan, commentator]
    game.add_observers(observers)
    game.play_ball()
    assert_true("assert over increment incorrect", game.overs == 0.1)
    assert_true("selects incorrect batter", game.batters[0] == game.get_current_batsman())
    game.play_ball()
    game.play_ball()
    game.play_ball()
    game.play_ball()
    game.play_ball()
    before_over_change_batters = game.batters
    runs = game.play_ball()
    after_over_change_batter = game.get_current_batsman()
    expected_batsman = before_over_change_batters[1] if runs % 2 == 0 else before_over_change_batters[0]
    assert_true("assert flips batters on over end", expected_batsman == after_over_change_batter)
    assert_true("assert notifies observers", len(commentator.memories) > 0 and len(fan.memory) > 0)


test_player_raises_exception_on_invalid_input()
test_team_assigns_batters_correctly()
# test_umpire_decides_correctly()
# test_observers_store_memories()
# test_game_plays_correctly_integration_test()

print(str(pass_count) + " / " + str(total_test_count) + " tests passed ")
