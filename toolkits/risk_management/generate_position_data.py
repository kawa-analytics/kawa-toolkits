from kywy.client.kawa_decorators import kawa_tool
import logging
import pandas as pd
import numpy as np
import yfinance as yf
from toolkits.risk_management.risk_management_common import STOCK_NAMES, TRADER_NAMES

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={},
    outputs={
        'stock': str,
        'trader': str,
        'notional': float,
        'quantity': float,
        'delta': float,
    },
)
def generate_position_data():
    data = []

    # Fetch the most recent market prices for each stock directly from Yahoo Finance
    latest_prices = {}
    for stock in STOCK_NAMES:
        stock_data = yf.download(stock, period='1d')

        if not stock_data.empty:
            latest_prices[stock] = stock_data['Close'].iloc[-1]  # Get the latest closing price

    for stock in STOCK_NAMES:
        for trader in TRADER_NAMES:
            quantity = np.random.randint(-50, 500)  # Random quantity between 100 and 10,000 shares
            price = latest_prices.get(stock, 0)  # Get the latest price for the stock
            notional = quantity * price  # Calculate notional based on quantity and latest price
            data.append({
                'stock': stock,
                'trader': trader,
                'notional': notional,
                'quantity': quantity,
                'delta': np.random.uniform(-1, 1)  # Random sensitivity
            })

    df = pd.DataFrame(data)
    logger.info('Position data was generated, it contains {} rows'.format(df.shape[0]))

    return df
