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
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    stock_list = df['stock'].tolist()

    var_95_df = pd.DataFrame()

    for stock in stock_list:
        # Fetch historical data from Yahoo Finance
        stock_data = yf.download(stock, start=start_date_str, end=end_date_str)

        # Calculate daily returns
        stock_data['Return'] = stock_data['Adj Close'].pct_change()
        stock_data = stock_data.dropna(subset=['Return'])

        # Calculate the 95th percentile (VaR 95) of daily returns
        if not stock_data['Return'].empty:
            var_95 = np.percentile(stock_data['Return'], 5)
        else:
            var_95 = np.nan

        var_95_df = var_95_df.append({'stock': stock, 'var95': var_95}, ignore_index=True)

    return var_95_df
