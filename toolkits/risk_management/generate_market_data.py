from kywy.client.kawa_decorators import kawa_tool
from datetime import datetime, date, timedelta
import logging
import pandas as pd
import yfinance as yf
import numpy as np

from toolkits.risk_management.risk_management_common import STOCK_NAMES, NUM_DAYS

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={},
    outputs={
        'date': date,
        'stock': str,
        'price': float,
        'volatility': float,
    },
)
def generate_market_data():
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=NUM_DAYS)

    data = []

    for stock in STOCK_NAMES:
        # Fetch historical market data from Yahoo Finance
        stock_data = yf.download(stock, start=start_date, end=end_date)

        # Check if data is fetched successfully
        if not stock_data.empty:
            stock_data.reset_index(inplace=True)
            stock_data['stock'] = stock  # Add stock ticker to each row
            stock_data = stock_data[['Date', 'stock', 'Close']]
            stock_data.rename(columns={
                'Date': 'date',
                'Close': 'price'}, inplace=True)

            # R

            for _, row in stock_data.iterrows():
                data.append({
                    'date': row['date'].date(),
                    'stock': row['stock'],
                    'price': row['price'],
                    'volatility': np.random.uniform(0.1, 0.5)
                })

    df = pd.DataFrame(data)
    logger.info('Market data was generated, it contains {} rows'.format(df.shape[0]))

    return df
