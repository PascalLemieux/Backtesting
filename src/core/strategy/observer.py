from abc import ABC, abstractmethod
from src.core.strategy.stateful import StatefulStrategy


class StrategyObserver(ABC):

    @abstractmethod
    def upon_notification(self, strategy: StatefulStrategy, *args, **kwargs):
        pass

