import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from scipy.stats import norm

NUM_STOCKS = 10
NUM_TRADERS = 5
NUM_TRADES = 100
NUM_DAYS = 252

STOCK_NAMES = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NVDA', 'JNJ', 'V']
TRADER_NAMES = ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Tom Davis']


def compute_premiums_and_greeks_on_date(position_data, market_data, target_date):
    """
    Compute premiums and Greeks for each option position on a given date based on provided market data.

    :param position_data: DataFrame with position data including option details.
    :param market_data: DataFrame with market data including 'date', 'stock', 'price', and 'vol' columns.
    :param target_date: Specific date to compute the premiums and Greeks for.
    :return: DataFrame with updated position data including calculated premium and Greeks.
    """
    results = []

    # Filter market data for the given date
    market_data_on_date = market_data[market_data['date'] == target_date]

    for index, position in position_data.iterrows():
        stock = position['stock']
        option_type = position['option_type']
        strike_price = position['strike_price']
        expiration_date = position['expiration_date']
        quantity = position['quantity']
        direction = position['direction']

        # Find the corresponding market data for the stock on the specified date
        market_row = market_data_on_date[market_data_on_date['stock'] == stock]

        if not market_row.empty:
            stock_price = market_row['price'].values[0]
            implied_volatility = market_row['volatility'].values[0]
            time_to_expiration = (expiration_date - target_date).days / 365

            # Calculate option premium and Greeks
            greeks = calculate_option_premium_and_greeks(
                S=stock_price, K=strike_price, T=time_to_expiration,
                r=0.01, sigma=implied_volatility, option_type=option_type
            )

            results.append({
                'trade_id': position['trade_id'],
                'risk_computation_date': target_date,
                'stock': stock,
                'trader': position['trader'],
                'option_type': option_type,
                'strike_price': strike_price,
                'expiration_date': expiration_date,
                'quantity': quantity,
                'direction': direction,
                'notional': position['notional'],
                'price': stock_price,
                'volatility': implied_volatility,
                'premium': greeks['premium'],
                'delta': greeks['delta'],
                'gamma': greeks['gamma'],
                'vega': greeks['vega'],
                'theta': greeks['theta'],
                'rho': greeks['rho']
            })

    return pd.DataFrame(results)


def calculate_option_premium_and_greeks(S, K, T, r, sigma, option_type):
    """
    Calculate the Black-Scholes option premium and Greeks.

    :param S: Current stock price
    :param K: Strike price
    :param T: Time to expiration in years
    :param r: Risk-free interest rate
    :param sigma: Volatility of the underlying stock
    :param option_type: 'call' or 'put'
    :return: Dictionary with premium, delta, gamma, vega, theta, and rho
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        premium = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        delta = norm.cdf(d1)
        theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    else:  # put option
        premium = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = -norm.cdf(-d1)
        theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)

    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100  # Vega is often expressed per 1% change in volatility

    return {
        'premium': premium,
        'delta': delta,
        'gamma': gamma,
        'vega': vega,
        'theta': theta,
        'rho': rho
    }


def fetch_real_time_price_and_volatility(price_increase_percent=0, vol_increase_percent=0):
    """
    Fetch the latest closing price and historical volatility for each stock in stock_names.

    :param stock_names: List of stock ticker symbols.
    :param num_days: Number of days to look back for historical data to calculate volatility.
    :return: DataFrame with columns ['date', 'stock', 'price', 'volatility'].
    """
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=10)

    data = []

    for stock in STOCK_NAMES:
        # Fetch historical market data from Yahoo Finance
        stock_data = yf.download(stock, start=start_date, end=end_date)

        # Check if data is fetched successfully
        if not stock_data.empty:
            # Calculate daily returns
            stock_data['daily_return'] = stock_data['Close'].pct_change()

            # Calculate historical volatility as the standard deviation of daily returns annualized
            volatility = stock_data['daily_return'].std() * np.sqrt(252)  # 252 trading days in a year

            # Get the latest closing price
            latest_price = stock_data['Close'].iloc[-1]

            # TR price
            rt_price = (latest_price
                        + latest_price * np.random.uniform(-0.01, 0.01)
                        + latest_price * price_increase_percent / 100)

            rt_vol = (volatility
                      + volatility * np.random.uniform(-0.01, 0.01)
                      + volatility * vol_increase_percent / 100)

            # Append the data to the list
            data.append({
                'date': end_date,
                'stock': stock,
                # Needs to be improved to generate fake real time data
                'price': rt_price,
                'volatility': rt_vol,
            })

    # Convert the data list to a DataFrame
    df = pd.DataFrame(data)
    return df
