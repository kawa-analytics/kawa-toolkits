from kywy.client.kawa_decorators import kawa_tool
import logging
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from scipy.stats import norm
from toolkits.risk_management.risk_management_common import STOCK_NAMES, TRADER_NAMES

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={},
    outputs={
        'stock': str,
        'trader': str,
        'option_type': str,
        'strike_price': float,
        'expiration_date': datetime,
        'quantity': float,
        'direction': str,
        'notional': float,
        'premium': float,
    },
)
def generate_position_data():
    # Fetch current stock prices and implied volatilities from Yahoo Finance
    stock_data = {}
    for stock in STOCK_NAMES:
        ticker = yf.Ticker(stock)
        stock_info = ticker.history(period="1d")
        stock_data[stock] = {
            'price': stock_info['Close'].iloc[-1],
            'implied_volatility': np.random.uniform(0.2, 0.4)  # Approximation if direct data isn't available
        }

    # Define option parameters
    option_types = ['call', 'put']
    directions = ['long', 'short']
    risk_free_rate = 0.01  # Example risk-free interest rate (1%)
    positions = []
    num_positions = 300
    for _ in range(num_positions):
        trader = np.random.choice(TRADER_NAMES)
        stock = np.random.choice(STOCK_NAMES)
        stock_price = stock_data[stock]['price']
        implied_volatility = stock_data[stock]['implied_volatility']
        option_type = np.random.choice(option_types)
        direction = np.random.choice(directions)
        strike_price = np.round(stock_price * np.random.uniform(0.8, 1.2),
                                2)  # Strike price within 20% of current price
        time_to_expiration = np.random.randint(30, 365) / 365  # Time to expiration in years
        expiration_date = datetime.today() + timedelta(days=int(time_to_expiration * 365))
        quantity = np.random.randint(1, 100)  # Random quantity between 1 and 100 contracts

        # Calculate the option premium using Black-Scholes model
        premium = calculate_option_premium(
            S=stock_price, K=strike_price, T=time_to_expiration,
            r=risk_free_rate, sigma=implied_volatility, option_type=option_type
        )

        # Calculate notional value based on strike price and quantity
        notional_value = strike_price * quantity * 100  # 100 shares per option contract

        positions.append({
            'stock': stock,
            'trader': trader,
            'option_type': option_type,
            'strike_price': strike_price,
            'expiration_date': expiration_date,
            'quantity': quantity,
            'direction': direction,
            'premium': premium,
            'notional': notional_value
        })

    position_data = pd.DataFrame(positions)
    return position_data


def calculate_option_premium(S, K, T, r, sigma, option_type):
    """
    Calculate the Black-Scholes option premium.

    :param S: Current stock price
    :param K: Strike price
    :param T: Time to expiration in years
    :param r: Risk-free interest rate
    :param sigma: Volatility of the underlying stock
    :param option_type: 'call' or 'put'
    :return: Option premium
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        premium = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:  # put option
        premium = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return premium
