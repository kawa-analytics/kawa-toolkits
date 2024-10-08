from kywy.client.kawa_decorators import kawa_tool
from datetime import date
import logging
import pandas as pd
import numpy as np
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
        'daily_pnl': float,
        'realized_pnl': float,
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
    unique_dates_sorted = unique_dates.sort_values(by='date', ascending=False)  # Sort dates in descending order
    recent_dates = unique_dates_sorted['date'].head(60)  # Get the 100 most recent dates
    recent_dates_sorted = recent_dates.sort_values(ascending=True)  # Sort these dates in ascending order for processing
    dfs = []

    previous_df = None
    for d in recent_dates_sorted:
        df = compute_premiums_and_greeks_on_date(position_data, market_data, target_date=d)
        df = df.sort_values(by='trade_id').reset_index(drop=True)

        # Calculate realized P&L for each trade
        df = pd.merge(df, position_data[['trade_id', 'initial_premium']], on='trade_id')

        df['realized_pnl'] = df.apply(
            lambda row: (row['premium'] - row['initial_premium']) * row['quantity'] * 100
            if row['direction'] == 'long' else (row['initial_premium'] - row['premium']) * row['quantity'] * 100,
            axis=1
        )

        if previous_df is not None:
            # Merge current and previous data on trade_id to calculate daily pnl
            merged_df = pd.merge(df, previous_df, on='trade_id', suffixes=('', '_prev'))
            merged_df['daily_pnl'] = (merged_df['premium'] - merged_df['premium_prev']) * merged_df['quantity'] * 100
            dfs.append(merged_df)
        else:
            # For the first entry, set daily pnl as NaN
            df['daily_pnl'] = np.nan
            dfs.append(df)

        previous_df = df  # Update the previous DataFrame to the current one

    histo_risk_df = pd.concat(dfs, ignore_index=True)

    # Drop unnecessary columns from the merge
    histo_risk_df = histo_risk_df.drop(columns=[col for col in histo_risk_df if col.endswith('_prev')])

    logger.info(histo_risk_df)

    return histo_risk_df
