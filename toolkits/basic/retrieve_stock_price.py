import yfinance as yf
import pandas as pd
from kywy.client.kawa_decorators import kawa_tool


@kawa_tool(
    inputs={'stock': str},
    outputs={'last_price': float},
)
def execute(df: pd.DataFrame) -> pd.DataFrame:
    df['last_price'] = df['stock'].apply(get_last_price)
    return df


def get_last_price(stock_symbol):
    try:
        ticker = yf.Ticker(stock_symbol)
        hist = ticker.history(period='1d')
        return 0 if hist.empty else hist['Close'].iloc[-1]
    except Exception as e:
        return 0
