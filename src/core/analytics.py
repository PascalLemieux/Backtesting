from src.core.execution import ExecutionEngine
from src.core.strategy.observer import StrategyObserver
from src.core.strategy.stateful import StatefulStrategy


class AnalyticsEngine(StrategyObserver):

    def __init__(self):
        self.realizations = []  # realizations of the same strategy

    def initialize(self, strategy: StatefulStrategy):
        # strategy.subscribe(self)
        pass

    def upon_notification(self, strategy: StatefulStrategy, *args, **kwargs):
        pass

    def aggregate(self, agent: ExecutionEngine):
        self.realizations.append(agent)
