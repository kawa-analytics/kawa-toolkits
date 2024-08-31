import datetime

import numpy as np
from kywy.client.kawa_client import KawaClient as K
from kywy.client.kawa_decorators import kawa_tool
from datetime import date, datetime
import logging
import pandas as pd

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={
        'trade_id': str,
        'instrument': str,
        'trade_date': datetime,
    },
    outputs={
        'insider_trade_detected': bool
    },
)
def insider_trade_detection(df, kawa):
    market_trades = df

    logger.info("Starting insider trade detection with:")
    logger.info(market_trades)

    news_data = (kawa
                 .sheet(sheet_name='News Data')
                 .select(
                    K.col('Instrument').alias('instrument'),
                    K.col('News Date').alias('news_date'),
                  )
                 .limit(-1)).compute()

    logger.info(news_data)

    # Merge data on the stock symbol (Instrument) to find trades around news events
    merged_data = pd.merge(market_trades, news_data, left_on='instrument', right_on='instrument', how='inner')

    # Calculate the time difference between trades and news events
    merged_data['time_difference'] = (merged_data['trade_date'] - merged_data['news_date']).dt.total_seconds()

    # Initialize the insider trade detection column to False
    merged_data['insider_trade_detected'] = False

    # Update the insider trade detection flag for trades that occurred within 1 day before a news event
    merged_data.loc[(merged_data['time_difference'] <= 0) & (
            merged_data['time_difference'] >= -86400), 'insider_trade_detected'] = True

    # Create a result DataFrame with Trade ID and Insider Trade Detected status
    result_df = merged_data[['trade_id', 'insider_trade_detected']]

    return result_df
