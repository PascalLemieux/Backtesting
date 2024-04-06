from abc import ABC, abstractmethod
from typing import List

from src.patterns.observer import Observable


class DataFeedObserver(ABC):

    @abstractmethod
    def upon_notification(self, feed, *args, **kwargs):
        raise NotImplementedError("Data feed observer notification handler not implemented")


class DataFeed(object):

    def __init__(self):
        self.observers: List[DataFeedObserver] = []

    def notify(self) -> None:
        """
        Notify all the observers for the arrival of a new data point.
        """
        for observer in self.observers:
            observer.upon_notification(self)

    def subscribe(self, subscriber: DataFeedObserver) -> None:
        """
        To attach a subscriber.
        """
        if subscriber not in self.observers:
            self.observers.append(subscriber)

    def unsubscribe(self, subscriber: DataFeedObserver) -> None:
        """
        To detach a subscriber.
        """
        if subscriber in self.observers:
            self.observers.remove(subscriber)

    def initialize(self) -> bool:
        """
        This will prepare the data flow, but not create notification.
        Observers will not be notified of new data points after initialization.

        The start/stop methods must be called upon for notifications management.
        """
        raise NotImplementedError("Specific to derived classes.")

    def start(self) -> None:
        """
        Starts the flow of notifications.
        """
        raise NotImplementedError("Specific to derived classes.")

    def stop(self) -> None:
        """
        Stops the flow of notifications.
        """
        raise NotImplementedError("Specific to derived classes.")

    def get_timestamp(self):
        """
        Provides the timestamp of the current data (price, volume, etc.)
        """
        raise NotImplementedError("Specific to derived classes.")

    def get_price_bid(self):
        """
        Provides the current bid price.
        """
        raise NotImplementedError("Specific to derived classes.")

    def get_price_ask(self):
        """
        Provides the current ask price.
        """
        raise NotImplementedError("Specific to derived classes.")

    def get_volume_bid(self):
        """
        Provides the current bid volume.
        """
        raise NotImplementedError("Specific to derived classes.")

    def get_volume_ask(self):
        """
        Provides the current ask volume.
        """
        raise NotImplementedError("Specific to derived classes.")