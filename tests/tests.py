import traceback
import sys

sys.path.append('src/')

from commentator import Commentator
from event import NotificationEvent, WinEvent, GameEvent
from fan import Fan
from innings import Inning
from notification import NotificationService
from player import Player
from position_tracker import PositionTracker
from scoreboard import Scoreboard
from team import Team
from umpire import out, not_out, is_batter_out

from player_statistics import PlayerStatistic, PlayerStatsService

pass_count = 0
total_test_count = 30


def test_passed():
    global pass_count
    global total_test_count
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


def test_position_tracker_assigns_batters_correctly():
    players = [Player("x", [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.04, 0.1]),
               Player("y", [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.04, 0.1]),
               Player("z", [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.04, 0.1]),
               Player("a", [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.04, 0.1])]
    batting_team = Team("xyz", players)
    bowling_team = Team("abc", [])
    player1 = players[0]
    player2 = players[1]
    player3 = players[2]

    event_out = NotificationEvent(1, player1, 0, True, 3, 10, 3, PlayerStatistic(player1))
    event_out2 = NotificationEvent(1, player2, 0, True, 3, 10, 3, PlayerStatistic(player1))
    event_out3 = NotificationEvent(1, player3, 0, True, 3, 10, 3, PlayerStatistic(player1))
    tracker = PositionTracker(batting_team, bowling_team)
    batter = tracker.select_first_batsman()
    next_batter = tracker.select_second_batsman()
    assert_true("invalid batter selected", batter == player1)
    assert_true("invalid alternate batter selected", next_batter == player2)

    tracker.notify(event_out)
    tracker.notify(event_out2)
    tracker.notify(event_out3)

    assert_exception(lambda x: tracker.select_first_batsman())
    assert_exception(lambda x: tracker.select_second_batsman())
    assert_exception(lambda x: tracker.select_current_batsman())

    tracker = PositionTracker(batting_team, bowling_team)
    is_out = True
    tracker.notify(NotificationEvent(1, player2, 0, is_out, 20, 20, 3, PlayerStatistic(player2)))
    assert_true("incorrect first batter on out", tracker.select_first_batsman() == player1)
    assert_true("incorrect second batter on out", tracker.select_second_batsman() == player3)
    assert_true("incorrect current batter on out", tracker.select_current_batsman() == player3)


def test_umpire_decides_correctly():
    assert_true("umpire does not notify when player is out", is_batter_out(out))
    assert_true("umpire makes player out when not out", not is_batter_out(not_out))


def test_observers_store_events():
    player = Player("x", [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.04, 0.1])
    player2 = Player("y", [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.04, 0.1])
    player3 = Player("z", [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.04, 0.1])
    commentator = Commentator()
    is_not_out = False
    event = NotificationEvent(1, player, 3, is_not_out, 10, 17, 3, PlayerStatistic(player))
    event2 = NotificationEvent(2, player2, 0, True, 9, 17, 2, PlayerStatistic(player2))
    event3 = NotificationEvent(3, player3, 1, is_not_out, 8, 16, 2, PlayerStatistic(player3))
    event4 = NotificationEvent(4, player, 2, is_not_out, 7, 14, 2, PlayerStatistic(player))
    commentator.notify(event)
    commentator.notify(event2)
    commentator.notify(event3)
    commentator.notify(event4)
    assert_true("commentator not storing events correctly", len(commentator.events) == 4)

    fan = Fan("xyz")
    fan.notify(event)
    fan.notify(event2)
    fan.notify(event3)
    fan.notify(event4)
    assert_true("fan not storing stats correctly", len(fan.stats) == 3)


def test_game_plays_correctly_integration_test():
    overs_left = 4
    runs_to_win = 40
    wickets_left = 3

    team_bangalore = Team("Lengaburu", [
        Player('Kirat Boli', [0.05, 0.3, 0.25, 0.1, 0.15, 0.01, 0.14, 0.0]),
        Player('N.S Nodhi', [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.14, 0.0]),
        Player('R Rumrah', [0.2, 0.3, 0.15, 0.05, 0.05, 0.01, 0.04, 0.2]),
        Player('Shashi Henra', [0.3, 0.25, 0.05, 0, 0.05, 0.01, 0.04, 0.3])
    ])

    team_chennai = Team("Enchai", [])
    game = Inning(team_bangalore, team_chennai, wickets_left, overs_left, number=2)
    game.update_runs_to_win(runs_to_win)

    fan = Fan(team_bangalore)
    commentator = Commentator()
    observers = [fan, commentator]
    game.add_observers(observers)
    runs = int(game.play_ball())
    assert_true("assert over increment incorrect", game.position_tracker.balls_played == 1)
    assert_true("selects incorrect batter", runs % 2 == game.position_tracker.current_batsman)
    game.play_ball()
    game.play_ball()
    game.play_ball()
    game.play_ball()
    game.play_ball()
    before_over_change_batters = [game.position_tracker.select_first_batsman(),
                                  game.position_tracker.select_second_batsman()]
    if game.position_tracker.current_batsman == 1:
        before_over_change_batters = list(reversed(before_over_change_batters))
    runs = int(game.play_ball())
    after_over_change_batter = game.select_current_batsman()
    expected_batsman = before_over_change_batters[0] if runs % 2 == 0 else before_over_change_batters[1]
    assert_true("assert flips batters on over end", expected_batsman == after_over_change_batter)
    assert_true("assert notifies observers", len(commentator.events) > 0 and len(fan.stats) > 0)


def test_notification_service_notifies_all_observers():
    notification_service = NotificationService()
    player = Player("x", [1, 0, 0, 0, 0, 0, 0, 0])
    player2 = Player("y", [0.5, 0.5, 0, 0, 0, 0, 0, 0])
    game = Inning(Team("xyz", [player, player2]), Team("abc", []),  3, 4, number=2)
    game.update_runs_to_win(20)
    game.play_ball()
    fan = Fan("xyz")
    commentator = Commentator()
    observers = [fan, commentator, game]
    notification_service.add_observers(observers)

    event = NotificationEvent(1, player, 1, False, 10, 17, 3, PlayerStatistic(player))
    notification_service.notify(event)
    assert_true("position tracker not notified", game.position_tracker.current_batsman == 1)
    assert_true("fan not notified", len(fan.stats) > 0)
    assert_true("commentator not notified", len(commentator.events) > 0)

    notification_service.notify_winner(WinEvent(Team("xyz", []), 1, 3, 0))
    assert_true("game not notified victory", game.winner)
    assert_true("fan not notified victory", fan.winner)
    assert_true("commentator not notified victory", commentator.winner)


def test_player_statistics_updates_correctly():
    player = Player("x", [1, 0, 0, 0, 0, 0, 0, 0, 0])
    player_stats_service = PlayerStatsService(Team("xyz", [player]))
    player_stats_service.add_statistic(player, 2, False)
    player_stats_service.add_statistic(player, 3, False)
    assert_true("player_statistics not being initialized", len(player_stats_service.player_statistics.keys()) > 0)
    assert_true("player_statistics not being updated", player_stats_service.player_statistics[player.name].runs == 5)


def test_scoreboard_works_correctly():
    overs_left = 4
    runs_to_win = 40
    wickets_left = 3

    kirat = Player('Kirat Boli', [0.05, 0.3, 0.25, 0.1, 0.15, 0.01, 0.09, 0.05])
    team_bangalore = Team("Lengaburu", [
        kirat,
        Player('N.S Nodhi', [0.1, 0.4, 0.2, 0.05, 0.1, 0.01, 0.04, 0.1]),
        Player('R Rumrah', [0.2, 0.3, 0.15, 0.05, 0.05, 0.01, 0.04, 0.2]),
        Player('Shashi Henra', [0.3, 0.25, 0.05, 0, 0.05, 0.01, 0.04, 0.3])
    ])

    team_chennai = Team("Enchai", [])

    scoreboard = Scoreboard(team_bangalore, team_chennai, wickets_left, overs_left, 2)
    scoreboard.update_runs_to_win(runs_to_win)
    fan = Fan("x")
    commentator = Commentator()
    scoreboard.add_observers([fan, commentator])
    scoreboard.notify(GameEvent(1, kirat, 2))
    assert_true("scoreboard not notifying observers on game events", len(fan.stats) > 0)
    assert_true("scoreboard not notifying observers on game events", len(commentator.events) > 0)
    assert_true("scoreboard not notifying observers correctly on game events: runs", commentator.events[0].runs == 2)
    assert_true("scoreboard not notifying observers correctly on game events: player name",
                commentator.events[0].batter.name == "Kirat Boli")
    scoreboard.notify(GameEvent(2, kirat, 100))
    assert_true("scoreboard not announcing winner on game end", fan.winner)


test_player_raises_exception_on_invalid_input()
test_position_tracker_assigns_batters_correctly()
test_umpire_decides_correctly()
test_observers_store_events()
test_game_plays_correctly_integration_test()
test_notification_service_notifies_all_observers()
test_player_statistics_updates_correctly()
test_scoreboard_works_correctly()

print(str(pass_count) + " / " + str(total_test_count) + " tests passed ")
