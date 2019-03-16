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


class Commentator:
    def __init__(self):
        self.memories = []

    def notify_score(self, over_count, batter, runs):
        self.memories = self.memories.append(Memory(over_count, batter, score_type, runs))

    def notify_out(self, over_count, batter):
        self.memories = self.memories.append(Memory(over_count, batter, out_type))

    def comment(self, memory):
        if memory.event_type == score_type:
            return str(memory.over_count) + " " + memory.batter.name + " scores " + str(memory.runs) + " " + (
                "runs" if memory.runs > 1 else "run"
            )
        elif memory.event_type == out_type:
            return str(memory.over_count) + " " + memory.batter.name + " is out"

    def commentary(self):
        return "\n".join([self.comment(memory) for memory in self.memories])


from collections import OrderedDict


class Observer:
    def __init__(self):
        self.memories = []
        self.summary = OrderedDict()

    def summarize_memory(self, memory):
        player = memory.batter
        player_name = player.name
        if player_name not in self.summary:
            self.summary[player_name] = (0, 1, player, not_out)
        runs, balls, out_status = self.summary[player_name]
        if memory.event_type == score_type:
            self.summary[player_name] = (runs + memory.runs, balls + 1, player, out_status)
        elif memory.event_type == out_type:
            self.summary[player_name] = (runs, balls + 1, is_out)

    def notify_score(self, over_count, batter, runs):
        memory = Memory(over_count, batter, score_type, runs)
        self.memories = self.memories.append(memory)
        self.summarize_memory(memory)

    def notify_out(self, over_count, batter):
        memory = Memory(over_count, batter, out_type)
        self.memories = self.memories.append(memory)
        self.summarize_memory(memory)

    def recall_summary(self, player_name):
        runs, balls, player, out_status = self.summary[player_name]
        return player_name + " - " + str(runs) + ("*" if out_status == not_out else "") + " (" + str(balls) + " balls)"

    def summarize_match(self):
        return "\n".join([self.recall_summary(player_name) for player_name in self.summary])
