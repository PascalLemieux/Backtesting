from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):

    @abstractmethod
    def upon_notification(self, *args, **kwargs):
        pass


class Observable(ABC):

    def __init__(self):
        self.observers: List[Observer] = []

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all the observers for the arrival of a new data point.
        """
        pass

    @abstractmethod
    def subscribe(self, subscriber: Observer) -> None:
        """
        To attach a subscriber.
        """
        pass

    @abstractmethod
    def unsubscribe(self, subscriber: Observer) -> None:
        """
        To detach a subscriber.
        """
        pass
