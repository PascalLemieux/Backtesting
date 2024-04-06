from src.core.feed.data import DataFeedObserver, DataFeed
from src.core.strategy.stateful import StatefulStrategy


class ExecutionEngine(DataFeedObserver):
    """
    This class wraps a strategy to provide execution. In order to provide a
    realistic behavior, the execution is aware of the market state.
    """

    def __init__(self, strategy: StatefulStrategy):
        self.strategy: StatefulStrategy = strategy

    def upon_notification(self, feed, *args, **kwargs):
        self.strategy.upon_notification(feed, *args, **kwargs)

    def initialize(self, data: DataFeed):
        data.subscribe(self)

    def trade(self, quantity: float, price: float = None):

        if quantity < 0.0:
            return self.trade_sell(quantity, price)

        elif quantity > 0.0:
            return self.trade_buy(quantity, price)

        else:
            pass

    def trade_buy(self, quantity: float, price: float = None):
        """
        Enters a buy order into the engine.

        Returns a tuple (quantity, price).
        """
        pass

    def trade_sell(self, quantity: float, price: float = None):
        """
        Enters a buy order into the engine.

        Returns a tuple (quantity, price).
        """
        pass
