from kywy.client.kawa_decorators import kawa_tool
from datetime import date
import logging
import pandas as pd
from kywy.client.kawa_client import KawaClient as K

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={},
    outputs={
        'date': date,
        'trader': str,
        'stock': str,
        'daily-pnl': float,
        'cumulative-pnl': float,
    },
)
def generate_historical_pnl_data(kawa):
    market_data = (kawa
                   .sheet(sheet_name='Market Data')
                   .select(K.cols())
                   .no_limit()
                   .compute())

    position_data = (kawa
                     .sheet(sheet_name='Position Data')
                     .select(K.cols())
                     .no_limit()
                     .compute())

    pnl_data = []

    for _, position in position_data.iterrows():
        stock = position['stock']
        trader = position['trader']
        quantity = position['quantity']

        stock_market_data = market_data[market_data['stock'] == stock].copy()
        stock_market_data['price_change'] = stock_market_data['price'].diff()

        stock_market_data['daily-pnl'] = stock_market_data['price_change'] * quantity
        stock_market_data['daily-pnl'] = stock_market_data['daily-pnl'].fillna(0)

        stock_market_data['cumulative-pnl'] = stock_market_data['daily-pnl'].cumsum()
        stock_market_data['trader'] = trader

        pnl_data.append(stock_market_data[['date', 'stock', 'trader', 'daily-pnl', 'cumulative-pnl']])

    pnl_df = pd.concat(pnl_data, ignore_index=True)

    return pnl_df
