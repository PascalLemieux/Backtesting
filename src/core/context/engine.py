from src.core.feed.data import DataFeed
from src.core.execution import ExecutionEngine
from src.core.analytics import AnalyticsEngine


class ContextualEngine(object):
    """
    This class groups together the various elements required for a backtest or for live trading:

    * The data feed (websocket or dataframe)
    * The strategy that will be called upon everytime the data feed provide an update
    * The analytics that will look at the performance of the strategy
    * The execution manager to handle trading

    """

    def __init__(self, data: DataFeed, agent: ExecutionEngine,
                 analytics: AnalyticsEngine, verbose: bool = False):
        #
        # Settings
        self.verbose: bool = verbose

        # Data Feed: to provide the input data
        self.data: DataFeed = data

        # Wrapped Strategy: to command financial execution
        self.agent: ExecutionEngine = agent

        # Analytics engine: to keep track of perf, risk, etc.
        self.analytics: AnalyticsEngine = analytics

        # Initialize the components
        self.initialize()

    def initialize(self):
        #
        # Initialize the strategy
        self.agent.initialize(self.data)
        print(f"Initializing {self.agent}")

        # Initialize the analytics
        self.analytics.initialize(strategy=self.agent.strategy)
        print(f"Initializing {self.analytics}")

        # Initialize the data feed
        self.data.initialize()
        print(f"Initializing {self.data}")

    def start(self, ):
        self.data.start()
        self.analytics.aggregate(self.agent)
        print(f"Backtest ended successfully.")
