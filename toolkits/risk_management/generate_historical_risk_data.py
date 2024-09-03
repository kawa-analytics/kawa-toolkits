from kywy.client.kawa_decorators import kawa_tool
from datetime import date
import logging
import pandas as pd
from kywy.client.kawa_client import KawaClient as K

from toolkits.risk_management.risk_management_common import compute_premiums_and_greeks_on_date

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={},
    outputs={
        'trade_id': str,
        'risk_computation_date': date,
        'stock': str,
        'trader': str,
        'option_type': str,
        'premium': float,
        'delta': float,
        'gamma': float,
        'vega': float,
        'theta': float,
        'rho': float,
    },
)
def generate_historical_risk_data(kawa):
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

    unique_dates = market_data[['date']].drop_duplicates()
    unique_dates_sorted = unique_dates.sort_values(by='date', ascending=False)
    recent_dates = unique_dates_sorted['date'].head(5)
    dfs = []
    for d in recent_dates:
        df = compute_premiums_and_greeks_on_date(position_data, market_data, target_date=d)
        dfs.append(df)

    histo_risk_df = pd.concat(dfs, ignore_index=True)

    return histo_risk_df
