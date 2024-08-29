import pandas as pd
import numpy as np
import yfinance as yf

from kywy.client.kawa_decorators import kawa_tool
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={'stock': str},
    outputs={'var95': float},
)
def calculate_var_95_last_month(df):
    # Calculate the date range for the past month
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)

    # Convert dates to string format required by yfinance
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Extract the list of stocks from the DataFrame
    stock_list = df['stocks'].tolist()

    # Create an empty list to store results
    results = []

    for stock in stock_list:
        # Fetch historical data from Yahoo Finance
        stock_data = yf.download(stock, start=start_date_str, end=end_date_str)

        # Calculate daily returns
        stock_data['Return'] = stock_data['Adj Close'].pct_change()

        # Drop NaN values from returns
        stock_data = stock_data.dropna(subset=['Return'])

        # Calculate the 95th percentile (VaR 95) of daily returns
        if not stock_data['Return'].empty:
            var_95 = np.percentile(stock_data['Return'], 5)
        else:
            var_95 = np.nan

        # Append the results to the list
        results.append({'Stock': stock, 'VaR_95': var_95})

    # Convert results list to DataFrame
    var_95_df = pd.DataFrame(results)

    return var_95_df
