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
        self.prev_update = None
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
        if len(self.ptf_protected_value) == 0:
            return True  # required for initialization
        return timestamp >= self.reset_freq + self.last_reset

    @property
    def last_reset(self):
        return list(sorted(self.price_reset.keys(), reverse=True))[0]

    @property
    def bond_value(self):
        if not len(self.ptf_value_history):
            return self.ptf_initial_value
        last_dt = list(sorted(self.riskfree_bond.keys(), reverse=True))[0]
        return self.riskfree_bond[last_dt]

    @property
    def exposure_value(self):
        last_dt = list(sorted(self.risky_exposure.keys(), reverse=True))[0]
        return self.risky_exposure[last_dt]

    @property
    def share_count(self):
        if not len(self.shares_owned):
            return 0.0
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

        # Avoids numerical jitter on floats
        price = 0.5 * (data_feed.get_price_bid() + data_feed.get_price_ask())
        price = round(price, 4)

        timestamp = data_feed.get_timestamp()
        if self.prev_update is None:
            self.prev_update = timestamp
            self.last_update = timestamp

        # Step back by 1 time step
        self.prev_update = self.last_update
        self.last_update = timestamp

        return self.update(price, timestamp)

    def update(self, price: float, timestamp: dt.datetime):

        # ############################################################
        # 1- Update (before): assessing our current portfolio
        # ############################################################

        # Keep track of time
        dt_ = max(0.0, (timestamp - self.prev_update).total_seconds() / SECONDS_PER_YEAR)

        # Record the asset price (always)
        self.asset_price[timestamp] = price

        # Bond interest accrued
        interests = self.bond_value * self.riskfree_rate * dt_

        # Risky exposure update
        prev_sh_count = self.share_count
        exposure = prev_sh_count * price

        # Total investments value
        ptf_total = exposure + self.bond_value + interests
        self.ptf_value_history[timestamp] = ptf_total

        # ############################################################
        # 2- Recompute (after): reviewing portfolio composition
        # ############################################################

        # Only on CPPI reset dates
        if self.is_reset(timestamp):

            # Store share price at which we reset
            self.price_reset[timestamp] = price

            # Update the level we protect
            prot_level_target = self.floor * ptf_total
            self.ptf_protected_value[timestamp] = prot_level_target

            # Re-compute exposure
            exposure_target = (ptf_total - prot_level_target) * self.multiplier

        else:  # just a regular update

            prot_level = self.ptf_protection
            self.ptf_protected_value[timestamp] = prot_level

            # Re-compute exposure: no leverage
            exposure_target = min(max(0.0, ptf_total - prot_level) * self.multiplier, ptf_total)

        # ############################################################
        # 2- Adjust (next time period): send for trading
        # ############################################################

        # Hence a new target number of shares
        sh_count = round(exposure_target / price, 6)
        self.shares_owned[timestamp] = sh_count

        # Start our bond investment (what's left after exposure)
        bond_target = max(0.0, ptf_total - exposure_target)
        self.riskfree_bond[timestamp] = bond_target





