from src.core.execution import ExecutionEngine
from src.core.analytics import AnalyticsEngine
from src.core.context.engine import ContextualEngine
from src.core.feed.monte_carlo import MonteCarloDataFeed
from src.cppi.strategy import CppiStrategy

if __name__ == '__main__':

    # Local CSV file
    #
    # 0: goes up
    # 1: ??

    path_ = "C:\\Users\\pace8\\PycharmProjects\\Backtesting\\dataset\\ou.csv"
    feed = MonteCarloDataFeed(csv_path=path_, columns=[1, ])

    cppi = CppiStrategy(floor=0.8, initial_value=100000.0)
    exec_cppi = ExecutionEngine(cppi)

    analytics = AnalyticsEngine()

    context = ContextualEngine(data=feed,
                               agent=exec_cppi,
                               analytics=analytics)

    # Start the backtest
    context.start()

    results = analytics.realizations
    print("The End.")

