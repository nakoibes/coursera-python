from abc import ABC, abstractmethod


class ObservableEngine(Engine):
    def __init__(self):
        self.subscribers = set()

    def subscribe(self, sub):
        self.subscribers.add(sub)

    def unsubscribe(self, sub):
        self.subscribers.remove(sub)

    def notify(self, ach):
        for sub in self.subscribers:
            sub.update(ach)


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, ach):
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, ach):
        self.achievements.add(ach['title'])


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = list()

    def update(self, ach):
        if ach not in self.achievements:
            self.achievements.append(ach)
