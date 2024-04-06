import datetime as dt
from typing import Optional

from src.core.context.exceptions import CausalityException


class TimeKeeper(object):

    def __init__(self, start_dt: dt.datetime = None):
        """
        Class managing the evolution of time during a simulation.
        """
        # Current date (our current filtration)
        self.current_dt: Optional[dt.datetime] = start_dt

        # Observations (time steps)
        self.obs_counter: int = -1

    @property
    def timestamp(self):
        if self.current_dt is None:
            raise NotImplementedError("TimeKeeper has not been initialized.")
        return dt.datetime(year=self.current_dt.year,  # boxed
                           month=self.current_dt.month,
                           day=self.current_dt.day,
                           hour=self.current_dt.hour,
                           minute=self.current_dt.minute,
                           second=self.current_dt.second)

    def reset(self, date: dt.datetime):
        self.current_dt = date
        self.obs_counter = -1

    def update(self, date: dt.date, *args, **kwargs):

        # Increment obs counter
        self.obs_counter += 1

        if self.current_dt is None:
            self.current_dt = date

        elif date <= self.current_dt:
            raise CausalityException("Going backward in time.")

        else:
            self.current_dt = date
