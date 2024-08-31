from kywy.client.kawa_decorators import kawa_tool
from datetime import datetime
import logging
import pandas as pd

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={
        'trade_id': str,
        'instrument': str,
        'trade_date': datetime,
        'trader_id': str,
    },
    outputs={
        'wash_trade_detected': bool
    },
)
def wash_trade_detection(df):
    market_trades = df

    market_trades['trade_date'] = pd.to_datetime(market_trades['trade_date'])

    # Identify trades with the same instrument by the same trader
    wash_trades = market_trades.groupby(['trader_id', 'instrument']).filter(lambda x: len(x) > 1)

    # Calculate time differences between trades for the same trader and instrument
    wash_trades['time_difference'] = wash_trades.groupby(['trader_id', 'instrument'])[
        'trade_date'].diff().dt.total_seconds()

    # Initialize the wash trade detection column to False
    wash_trades['Wash Trade Detected'] = False

    # Update the wash trade detection flag for trades that occurred within 5 minutes
    wash_trades.loc[
        (wash_trades['time_difference'] <= 300) & (wash_trades['time_difference'] > 0), 'wash_trade_detected'] = True

    # Create a result DataFrame with Trade ID and Wash Trade Detected status
    result_df = wash_trades[['trade_id', 'wash_trade_detected']]

    return result_df
