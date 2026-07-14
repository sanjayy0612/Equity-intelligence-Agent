# market_data.py
# The single seam over OpenBB. Every tool asks for data here and never touches
# `obb`, provider strings, `.results[0]`, or `model_dump()` directly. Swapping the
# data provider (yfinance -> something else) is a one-file change.
from openbb import obb

PROVIDER = "yfinance"


def metrics(symbol: str) -> dict | None:
    """Fundamental metrics for a ticker as a plain dict, or None if unavailable."""
    res = obb.equity.fundamental.metrics(symbol, provider=PROVIDER)
    return res.results[0].model_dump() if res.results else None


def profile(symbol: str) -> dict | None:
    """Company profile for a ticker as a plain dict, or None if unavailable."""
    res = obb.equity.profile(symbol, provider=PROVIDER)
    return res.results[0].model_dump() if res.results else None


def price_history(symbol: str):
    """Historical price data for a ticker as a DataFrame."""
    return obb.equity.price.historical(symbol, provider=PROVIDER).to_dataframe()
