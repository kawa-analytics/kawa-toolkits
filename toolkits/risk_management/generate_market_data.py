from kywy.client.kawa_decorators import kawa_tool
from datetime import datetime, date
import logging
import pandas as pd
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
    dates = pd.date_range(end=datetime.today(), periods=NUM_DAYS).to_pydatetime().tolist()
    data = []

    for stock in STOCK_NAMES:
        price = 100 + np.cumsum(np.random.randn(NUM_DAYS))  # Random walk for stock prices
        volatility = np.random.uniform(0.1, 0.5)  # Random volatility between 10% and 50%
        for i in range(NUM_DAYS):
            data.append({
                'Date': dates[i],
                'Stock': stock,
                'Price': price[i],
                'Volatility': volatility
            })

    df = pd.DataFrame(data)
    logger.info('Market data was generated, it contains {} rows'.format(df.shape[0]))

    return df
