import pandas as pd
import datetime as dt
from typing import Optional
from src.core.feed.data import DataFeed
from src.core.context.schedule import TimeKeeper


class MonteCarloDataFeed(DataFeed):

    def __init__(self, csv_path, columns=None):
        super().__init__()
        self.file_path = csv_path
        self.dataset: Optional[pd.DataFrame] = None
        self.columns = columns if columns is not None else [0, ]

        # Fields to be queried by observers
        self.time = TimeKeeper()
        self.price: Optional[float] = None

        self.initialize()

    def initialize(self) -> bool:
        # Load the dataframe from disk
        df = pd.read_csv(self.file_path)

        # Set a correct time index
        df["Index"] = pd.to_datetime(df["Date"])

        # Set index to the datetime objects
        df.set_index('Index', inplace=True)

        # Remove excess date column (str)
        df.drop(columns=["Date"], inplace=True)

        # Clean up the column names
        df.columns = [int(c) for c in df.columns]

        # Set dataset locally
        self.dataset = df

        # Confirm we're good
        return True

    def get_timestamp(self):
        return self.time.timestamp

    def get_price_bid(self):
        return self.price

    def get_price_ask(self):
        return self.price

    def get_volume_bid(self):
        return 1e9  # ignoring volume for now

    def get_volume_ask(self):
        return 1e9

    def start(self) -> None:

        if not len(self.dataset):
            self.initialize()

        # The column(s) we're using
        col = self.columns

        # Start our timekeeper
        epsilon = dt.timedelta(seconds=1.0)
        self.time.reset(date=self.dataset.index.min() - epsilon)

        for k in range(len(self.dataset)):

            # Update current time
            self.time.update(self.dataset.index[k])

            # Update the current price (only mid)
            self.price = self.dataset[col].iloc[k].to_numpy()[0]  # assumes only closing px

            # Notify observers
            self.notify()
