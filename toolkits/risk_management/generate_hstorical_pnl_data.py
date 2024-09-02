from kywy.client.kawa_decorators import kawa_tool
from datetime import datetime, date, timedelta
import logging
import pandas as pd
import numpy as np

from toolkits.risk_management.risk_management_common import NUM_DAYS, TRADER_NAMES

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={},
    outputs={
        'date': date,
        'trader': str,
        'daily-pnl': float,
        'cumulative-pnl': float,
    },
)
def generate_historical_pnl_data():
    dates = [datetime.today().date() - timedelta(days=i) for i in range(NUM_DAYS)]
    data = []

    for trader in TRADER_NAMES:
        pnl = 0
        for i in range(NUM_DAYS):
            daily_pnl = np.random.normal(0, 10000)  # Daily PnL with mean 0 and std dev $10k
            pnl += daily_pnl
            data.append({
                'date': dates[i],
                'trader': trader,
                'daily-pnl': daily_pnl,
                'cumulative-pnl': pnl
            })

    df = pd.DataFrame(data)
    logger.info('PnL data was generated, it contains {} rows'.format(df.shape[0]))
    return df
