from kywy.client.kawa_decorators import kawa_tool
from datetime import date
import logging
import pandas as pd
import numpy as np

@kawa_tool(
    inputs={
        'stock':str,
        'date': date,
        'price': float,
    },
    outputs={
        'volatility': float,
    },
)
def generate_market_data(df):
    window = 30
    market_data = df.sort_values(by=['stock', 'date']).reset_index(drop=True)

    # Initialize a DataFrame to store volatility results
    volatility_df = pd.DataFrame()

    # Group market data by stock and compute rolling volatility for each stock
    for stock, stock_data in market_data.groupby('stock'):
        # Calculate daily returns using log returns
        stock_data['daily_return'] = np.log(stock_data['price'] / stock_data['price'].shift(1))

        # Compute the rolling standard deviation of daily returns
        stock_data['rolling_volatility'] = stock_data['daily_return'].rolling(window=window).std()

        # Annualize the rolling volatility
        stock_data['rolling_volatility'] = stock_data['volatility'] * np.sqrt(252)

        # Select relevant columns
        stock_data = stock_data[['date', 'stock', 'volatility']]

        # Append the result to the final DataFrame
        volatility_df = pd.concat([volatility_df, stock_data], ignore_index=True)

    return volatility_df

