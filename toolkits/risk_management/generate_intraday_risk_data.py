from kywy.client.kawa_decorators import kawa_tool
from datetime import date, datetime
import logging
import pandas as pd
from kywy.client.kawa_client import KawaClient as K

from toolkits.risk_management.risk_management_common import compute_premiums_and_greeks_on_date, \
    fetch_real_time_price_and_volatility

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={
        'trade_id': str,
        'price_increase_percent': float,
        'vol_increase_percent': float,
        'stock': str,
        'strike_price': float,
        'notional': float,
        'trader': str,
        'expiration_date': date,
        'quantity': float,
        'direction': str,
        'option_type': str,
    },
    outputs={
        'daily_pnl': float,
        'delta_pnl': float,
        'gamma_pnl': float,
        'vega_pnl': float,
        'theta_pnl': float,
        'rho_pnl': float,
    },
)
def generate_intraday_risk_data(df, kawa):
    today = datetime.today().date()
    pnl_results = []
    position_data = df

    # D market and greeks data
    intraday_market_data = fetch_real_time_price_and_volatility()
    intraday_risk_data = compute_premiums_and_greeks_on_date(
        position_data=position_data,
        market_data=intraday_market_data,
        target_date=today,
    )

    # D-1 market and greeks data
    historical_market_data = (kawa
                              .sheet(sheet_name='Market Data')
                              .select(K.cols())
                              .no_limit()
                              .compute())

    historical_greeks_data = (kawa
                              .sheet(sheet_name='Histo Risk Data')
                              .select(K.cols())
                              .no_limit()
                              .compute())

    unique_dates = historical_market_data[['date']].drop_duplicates()
    unique_dates_sorted = unique_dates.sort_values(by='date', ascending=False)
    recent_dates = unique_dates_sorted['date'].head(5)
    most_recent_date = max(recent_dates)

    latest_historical_data_row = historical_market_data[historical_market_data['date'] == most_recent_date]
    latest_greeks_data_row = historical_greeks_data[
        historical_greeks_data['risk_computation_date'] == most_recent_date]

    for _, position in position_data.iterrows():
        # Load position fields
        r = 0.01
        stock = position['stock']
        quantity = position['quantity']
        trade_id = position['trade_id']

        current_market_data_row = intraday_market_data[intraday_market_data['stock'] == stock]
        current_greeks_row = intraday_risk_data[intraday_risk_data['trade_id'] == trade_id]

        historical_market_data_row = latest_historical_data_row[latest_historical_data_row['stock'] == stock]
        historical_greeks_row = latest_greeks_data_row[latest_greeks_data_row['trade_id'] == trade_id]

        if (not historical_market_data_row.empty and
                not current_market_data_row.empty and
                not historical_greeks_row.empty and
                not current_greeks_row.empty):
            hist_price = historical_market_data_row['price'].values[0]
            hist_vol = historical_market_data_row['volatility'].values[0]

            curr_price = current_market_data_row['price'].values[0]
            curr_vol = current_market_data_row['volatility'].values[0]

            greeks_hist = historical_greeks_row.iloc[0]
            greeks_cur = current_greeks_row.iloc[0]

            daily_pnl = (greeks_cur['premium'] - greeks_hist['premium']) * quantity * 100

            # Risk Based PNL
            delta_pnl = greeks_hist['delta'] * (curr_price - hist_price) * quantity * 100
            gamma_pnl = 0.5 * greeks_hist['gamma'] * ((curr_price - hist_price) ** 2) * quantity * 100
            vega_pnl = greeks_hist['vega'] * (curr_vol - hist_vol) * quantity * 100
            theta_pnl = greeks_hist['theta'] * quantity * 100
            rho_pnl = greeks_hist['rho'] * (r - 0.01) * quantity * 100

            pnl_results.append({
                'trade_id': trade_id,
                'stock': stock,
                'daily_pnl': daily_pnl,
                'delta_pnl': delta_pnl,
                'gamma_pnl': gamma_pnl,
                'vega_pnl': vega_pnl,
                'theta_pnl': theta_pnl,
                'rho_pnl': rho_pnl,
                'price D-1': hist_price,
                'price D': curr_price,
            })

    return pd.DataFrame(pnl_results)
