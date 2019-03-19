class Observer:
    def __init__(self):
        self.events = []
        self.winner = False

    def notify(self, notification_event):
        self.events = [*self.events, notification_event]

    def notify_winner(self, win_event):
        self.winner = win_event
