import datetime as dt
import time

from src.core.execution import ExecutionEngine
from src.core.analytics import AnalyticsEngine
from src.core.context.engine import ContextualEngine
from src.core.feed.monte_carlo import MonteCarloDataFeed
from src.cppi.strategy import CppiStrategy

if __name__ == '__main__':
    import time

    from multiprocessing import Pool, cpu_count
    from paths import GeometricBrownianMotion
    from src.core.context.engine import start_bt

    # Local CSV file
    #
    # 0: goes up
    # 1: ??
    """
    path_ = "C:\\Users\\pace8\\PycharmProjects\\Backtesting\\dataset\\ou.csv"
    feed = MonteCarloDataFeed(path_, columns=[1, ])
    
    
    cppi = CppiStrategy(floor=0.8,
                        initial_value=100000.0,
                        reset_freq=dt.timedelta(days=10))

    exec_cppi = ExecutionEngine(cppi)

    analytics = AnalyticsEngine()

    context = ContextualEngine(data=feed,
                               agent=exec_cppi,
                               analytics=analytics)

    # Start the backtest
    context.start()
    """
    st_time = time.time()
    mc_paths = 500
    maturity = 5.0
    time_intervals = maturity * 365

    gbm = GeometricBrownianMotion(volatility=0.60,
                                  drift=0.20,
                                  initial_value=100.0,
                                  maturity=maturity,
                                  time_intervals=int(time_intervals),
                                  seed=40)
    gbm.generate(mc_paths)
    df_paths = gbm.to_datetime_index()

    analytics = AnalyticsEngine()
    bts = []

    for i in range(df_paths.shape[1]):
        feed_i = MonteCarloDataFeed(df_paths, columns=[i, ])
        cppi = CppiStrategy(floor=0.80,
                            initial_value=100000.0,
                            reset_freq=dt.timedelta(days=100))

        agent_cppi_i = ExecutionEngine(cppi)

        backtest_i = ContextualEngine(data=feed_i,
                                      agent=agent_cppi_i,
                                      analytics=analytics)
        bts.append(backtest_i)

    pool = Pool()
    pool.map(start_bt, bts)

    print(f"The End, after {time.time()-st_time:.2f} seconds.")



    # 100: 12
    # 500: 55
