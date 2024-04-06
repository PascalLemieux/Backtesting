from abc import ABC, abstractmethod
from typing import List

from src.core.feed.data import DataFeedObserver


class StrategyObserver(ABC):

    @abstractmethod
    def upon_notification(self, strategy, *args, **kwargs):
        raise NotImplementedError("Strategy observer notification handler not implemented")


class StatefulStrategy(DataFeedObserver):
    """
    Base class for strategies.

    Contains basic logic for strategies running along a given
    Monte Carlo path or along a single realization (live feed).
    """

    def __init__(self, verbose: bool = False):
        self.verbose: bool = verbose
        self.observers: List[StrategyObserver] = []

    def upon_notification(self, data_feed, *args, **kwargs):
        """
        For the subscription to the ** data feed **.

        :param data_feed: Data feed
        :param args: n/a
        :param kwargs: n/a
        :return: None
        """
        raise NotImplementedError("Must implement upon_notification method")

    def notify(self) -> None:
        """
        Notify all ** strategy ** observers for the arrival of a new data point.
        """
        for observer in self.observers:
            observer.upon_notification(self)

    def subscribe(self, subscriber: StrategyObserver) -> None:
        """
        To attach a ** strategy ** subscriber.
        """
        if subscriber not in self.observers:
            self.observers.append(subscriber)

    def unsubscribe(self, subscriber: StrategyObserver) -> None:
        """
        To detach a ** strategy **  subscriber.
        """
        if subscriber in self.observers:
            self.observers.remove(subscriber)