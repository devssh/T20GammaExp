from collections import OrderedDict
from umpire import is_out, not_out
from game import number_of_balls_in_over

score_type = "score"
out_type = "out"
winner_summary_type = "winner"
initial_conditions_type = "conditions"


class Memory:
    def __init__(self, over_count, batter, event_type, runs=0):
        self.over_count = over_count
        self.batter = batter
        self.event_type = event_type
        self.runs = runs

    def __str__(self):
        if self.event_type == score_type:
            return str(self.over_count) + " " + self.batter.name + " scores " + str(self.runs) + " " + (
                "runs" if self.runs > 1 else "run"
            )
        elif self.event_type == out_type:
            return str(self.over_count) + " " + self.batter.name + " is out"

    def __repr__(self):
        return self.__str__()


class Commentator:
    def __init__(self, overs_left, runs_to_win, wickets_left):
        self.runs_to_win = runs_to_win
        self.overs_left = overs_left
        self.wickets_left = wickets_left
        self.memories = []
        self.winner = ""

    def notify_score(self, over_count, batter, runs):
        self.memories = [*self.memories, Memory(over_count, batter, score_type, runs)]

    def notify_out(self, over_count, batter):
        self.memories = [*self.memories, Memory(over_count, batter, out_type, 0)]

    def notify_winner(self, winning_team):
        self.winner = winning_team.name

    def commentary(self):
        commentary = ""
        balls_played = 0
        runs = 0
        for memory in self.memories:
            if balls_played % number_of_balls_in_over == 0:
                commentary = commentary + "\n" + str(
                    int(self.overs_left - (balls_played / number_of_balls_in_over))) + " overs left. " + str(
                    self.runs_to_win - runs
                ) + " runs to win"
            balls_played = balls_played + 1
            runs = runs + memory.runs
            commentary = commentary + "\n" + str(memory)
        commentary = commentary + "\n" + self.winner + " won by x wickets and y balls remaining"
        return commentary


class StatisticalMemory:
    def __init__(self, runs, balls_played, player, out_status):
        self.out_status = out_status
        self.player = player
        self.balls_played = balls_played
        self.runs = runs

    def add_memory(self, memory):
        self.out_status = memory.event_type
        self.runs = self.runs + memory.runs
        self.balls_played = self.balls_played + 1
        return self

    def __str__(self):
        player_name = self.player.name
        return player_name + " - " + str(self.runs) + (
            "*" if self.out_status == not_out else ""
        ) + " (" + str(self.balls_played) + " balls)"

    def __repr__(self):
        return self.__str__()


class Fan:
    def __init__(self, team_to_support):
        self.team_to_support = team_to_support
        self.memory = OrderedDict()
        self.winner = ""

    def summarize_memory(self, memory):
        player = memory.batter
        player_name = player.name
        if player_name not in self.memory:
            self.memory[player_name] = StatisticalMemory(0, 1, player, not_out)
        old_memory = self.memory[player_name]
        if memory.event_type == score_type:
            self.memory[player_name] = old_memory.add_memory(memory)
        elif memory.event_type == out_type:
            self.memory[player_name] = old_memory.add_memory(memory)

    def notify_score(self, over_count, batter, runs):
        memory = Memory(over_count, batter, score_type, runs)
        self.summarize_memory(memory)

    def notify_out(self, over_count, batter):
        memory = Memory(over_count, batter, out_type)
        self.summarize_memory(memory)

    def notify_winner(self, winning_team):
        self.winner = winning_team.name

    def recall_summary(self, player_name):
        runs, balls, player, out_status = self.memory[player_name]
        return player_name + " - " + str(runs) + ("*" if out_status == not_out else "") + " (" + str(balls) + " balls)"

    def summarize_match(self):
        return "\n".join([self.recall_summary(player_name) for player_name in self.memory])
