import pandas as pd

from src.core.execution import ExecutionEngine
from src.core.strategy.observer import StrategyObserver


class AnalyticsEngine(StrategyObserver):

    def __init__(self):
        self.realizations = []  # realizations of the same agent

    def initialize(self, agent: ExecutionEngine):
        # strategy.subscribe(self)
        pass

    def upon_notification(self, agent: ExecutionEngine, *args, **kwargs):
        pass

    def store(self, agent: ExecutionEngine):
        self.realizations.append(agent)

    @classmethod
    def summarize(cls, agent: ExecutionEngine):

        # Get ref to strategy
        strategy = agent.strategy

        # Assume the portfolio history contains
        # all dates observed during the simulation
        ptf = list(strategy.ptf_value_history.values())
        idx = list(strategy.ptf_value_history.keys())

        # Price of the underlying asset
        px = list(strategy.asset_price.values())

        # Protection level of the CPPI
        prot = list(strategy.ptf_protected_value.values())

        df = pd.DataFrame({"CPPI": ptf, "Protection": prot, "Undl": px}, index=idx)
        ts_init = df.index.min()
        df["Protection"] = df["Protection"] / df["CPPI"][ts_init]
        df["CPPI"] = df["CPPI"] / df["CPPI"][ts_init]
        df["Undl"] = df["Undl"] / df["Undl"][ts_init]
        return df

