import yfinance as yf
import pandas as pd
from kywy.client.kawa_decorators import kawa_tool


@kawa_tool(
    inputs={},
    outputs={'stock': str, 'last_price': float},
)
def execute() -> pd.DataFrame:
    stock_symbols = ['AAPL', 'TSLA', 'MSFT', 'CSCO', 'META', 'AMZN', 'GOOGL', 'NVDA']
    prices = []
    symbols = []
    for symbol in stock_symbols:
        try:
            stock = yf.Ticker(symbol)
            stock_price = stock.history(period="1d")['Close'].iloc[-1]  # Get the last close price
            symbols.append(symbol)
            prices.append(stock_price)
        except Exception as e:
            print(f"Failed to retrieve data for {symbol}: {e}")

    df = pd.DataFrame({
        'stock': symbols,
        'last_price': prices
    })

    return df
