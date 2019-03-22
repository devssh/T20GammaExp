from observer import Observer


class NotificationService(Observer):
    def __init__(self):
        super().__init__()
        self.observers = []

    def add_observers(self, observers):
        self.observers = [*self.observers, *observers]

    def notify(self, event):
        [observer.notify(event) for observer in self.observers]

    def notify_winner(self, win_event):
        [observer.notify_winner(win_event) for observer in self.observers]
