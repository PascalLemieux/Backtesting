import datetime as dt
from src.core.strategy.stateful import StatefulStrategy

SECONDS_PER_YEAR = 365.25 * 24 * 60 * 60


class CppiStrategy(StatefulStrategy):

    def __init__(self, floor: float, multiplier: float = None, initial_value: float = None,
                 reset_freq: dt.timedelta = None, verbose: bool = False):

        # Init parent class
        super().__init__(verbose=verbose)

        # Input characteristics
        self.floor = max(0.0, floor)  # percent
        self.multiplier = max(0.0, multiplier) if multiplier is not None else 1.0 / (1.0 - self.floor)

        # No fixed maturity
        self.reset_freq = reset_freq if reset_freq is not None else dt.timedelta(days=365*1000)

        # Hurdle rates
        self.riskfree_rate = 0.05

        # Previous update timestamp
        self.last_update = None

        # Portfolio (ptf) characteristics
        self.ptf_initial_value = max(0.0, initial_value) if initial_value is not None else 1.0

        # The protected levels (intended to reset evey quarter, e.g.)
        self.ptf_protected_value = {}  # Ptf value at reset dates
        self.price_reset = {}  # Price at reset dates

        # Track record (every step)
        self.ptf_value_history = {}
        self.risky_exposure = {}
        self.shares_owned = {}
        self.asset_price = {}
        self.riskfree_bond = {}

    def is_reset(self, timestamp):
        return timestamp > self.reset_freq + self.last_reset

    @property
    def last_reset(self):
        return list(sorted(self.price_reset.keys(), reverse=True))[0]

    @property
    def bond_value(self):
        last_dt = list(sorted(self.riskfree_bond.keys(), reverse=True))[0]
        return self.riskfree_bond[last_dt]

    @property
    def exposure_value(self):
        last_dt = list(sorted(self.risky_exposure.keys(), reverse=True))[0]
        return self.risky_exposure[last_dt]

    @property
    def share_count(self):
        last_dt = list(sorted(self.shares_owned.keys(), reverse=True))[0]
        return self.shares_owned[last_dt]

    @property
    def ptf_value(self):
        last_dt = list(sorted(self.ptf_value_history.keys(), reverse=True))[0]
        return self.ptf_protected_value[last_dt]

    @property
    def ptf_protection(self):
        last_dt = list(sorted(self.ptf_protected_value.keys(), reverse=True))[0]
        return self.ptf_protected_value[last_dt]

    def upon_notification(self, data_feed, *args, **kwargs):
        print(f"CPPI strategy got a data feed notification.")
        price = 0.5 * (data_feed.get_price_bid() + data_feed.get_price_ask())
        timestamp = data_feed.get_timestamp()
        return self.update(price, timestamp)

    def update(self, price: float, timestamp: dt.datetime):

        if len(self.price_reset) == 0:

            # Keep track
            self.last_update = timestamp

            # Amount protected from start
            self.ptf_protected_value[timestamp] = self.ptf_initial_value * self.floor

            # Cushion
            cushion = (1.0 - self.floor) * self.ptf_initial_value  # special case at init

            # Share count
            sh_count = cushion * self.multiplier / price
            self.shares_owned[timestamp] = sh_count

            # Record the asset price
            self.asset_price[timestamp] = price
            self.price_reset[timestamp] = price

            # Exposure
            exposure = sh_count * price
            self.risky_exposure[timestamp] = exposure

            # Start our bond investment (what's left after exposure)
            bond_investment = self.ptf_initial_value - exposure
            self.riskfree_bond[timestamp] = bond_investment

            # Update the track record
            self.ptf_value_history[timestamp] = exposure + bond_investment

            print(f"CPPI strategy started at {timestamp}.")

        elif self.is_reset(timestamp):

            # Keep track of time
            dt_ = (timestamp - self.last_update).total_seconds() / SECONDS_PER_YEAR
            self.last_update = timestamp

            # Bond interest accrued
            interests = self.bond_value * self.riskfree_rate * dt_

            # Record the asset price
            self.asset_price[timestamp] = price
            self.price_reset[timestamp] = price

            # Risky exposure update
            exposure = self.share_count * price

            # Before reset, we observed a total value
            ptf_total = exposure + self.bond_value + interests
            self.ptf_value_history[timestamp] = ptf_total

            # Update the level we protect
            new_prot_level = self.floor * ptf_total
            self.ptf_protected_value[timestamp] = new_prot_level

            # Re-compute exposure
            new_exposure = (ptf_total - new_prot_level) * self.multiplier

            # Hence a new target number of shares
            sh_count = new_exposure / price
            self.shares_owned[timestamp] = sh_count

            # Bond investment update
            new_bond_investment = ptf_total - new_prot_level
            self.riskfree_bond[timestamp] = new_bond_investment

        else:
            # Keep track of time
            dt_ = (timestamp - self.last_update).total_seconds() / SECONDS_PER_YEAR
            self.last_update = timestamp

            # Bond interest accrued
            interests = self.bond_value * self.riskfree_rate * dt_

            # Record the asset price
            self.asset_price[timestamp] = price

            # Risky exposure update
            exposure = self.share_count * price

            # Total investments value
            ptf_total = exposure + self.bond_value + interests
            self.ptf_value_history[timestamp] = ptf_total

            # Re-compute exposure: no leverage
            new_exposure = min(max(0.0, ptf_total - self.ptf_protection) * self.multiplier, ptf_total)

            # Hence a new target number of shares
            sh_count = new_exposure / price
            self.shares_owned[timestamp] = sh_count

            # Start our bond investment (what's left after exposure)
            bond_investment = ptf_total - new_exposure
            self.riskfree_bond[timestamp] = bond_investment







