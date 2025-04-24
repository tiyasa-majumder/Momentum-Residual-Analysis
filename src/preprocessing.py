import pandas as pd
import numpy as np

def calculate_returns(prices):
    """
    Calculate monthly returns from price data.
    """
    return prices.pct_change(fill_method=None)