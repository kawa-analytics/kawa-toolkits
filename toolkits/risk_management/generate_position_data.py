from kywy.client.kawa_decorators import kawa_tool
import logging
import pandas as pd
import numpy as np

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

    for stock in STOCK_NAMES:
        for trader in TRADER_NAMES:
            notional = np.random.randint(1e5, 1e7)  # Random notional between $100k and $10M
            quantity = np.random.randint(100, 10000)  # Random quantity between 100 and 10,000 shares
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
