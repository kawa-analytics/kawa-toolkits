from kywy.client.kawa_decorators import kawa_tool
import logging
import pandas as pd
import numpy as np
import yfinance as yf
import uuid
from datetime import datetime, timedelta, date
from scipy.stats import norm
from toolkits.risk_management.risk_management_common import STOCK_NAMES, TRADER_NAMES, \
    calculate_option_premium_and_greeks

logger = logging.getLogger('script-logger')

"""
1) Portfolio = position
2) Market data
3) Risk Histo -> premium + greeks
4) Intraday Risk ->  premium + greeks (computed with current market data) - Introduce variations

In the portfolio sheet:
1) Computed PnL (premium(intraday) - premium(latest in risk histo))
2) Risk Based PnL (Black-Scholes model with price and vol)


"""


@kawa_tool(
    inputs={},
    outputs={
        'trade_id': str,
        'stock': str,
        'trader': str,
        'option_type': str,
        'strike_price': float,
        'expiration_date': date,
        'quantity': float,
        'direction': str,
        'notional': float,
        'trade_date': date,
        'initial_premium': float,
    },
)
def generate_position_data():
    stock_data = {}
    for stock in STOCK_NAMES:
        ticker = yf.Ticker(stock)
        stock_info = ticker.history(period="1d")
        stock_data[stock] = {
            'price': stock_info['Close'].iloc[-1]
        }

    # Define option parameters
    option_types = ['put', 'put']
    directions = ['long', 'long', 'long']
    risk_free_rate = 0.01  # Example risk-free interest rate (1%)
    volatility = 0.2
    positions = []
    num_positions = 300

    for _ in range(num_positions):
        trader = np.random.choice(TRADER_NAMES)
        stock = np.random.choice(STOCK_NAMES)
        stock_price = stock_data[stock]['price']
        option_type = np.random.choice(option_types)
        direction = np.random.choice(directions)
        strike_price = np.round(stock_price * np.random.uniform(0.5, 0.7),
                                2)  # Strike price within 20% of current price
        time_to_expiration = np.random.randint(30, 365) / 365  # Time to expiration in years
        expiration_date = (datetime.today() + timedelta(days=int(time_to_expiration * 365))).date()
        quantity = np.random.randint(1, 100)  # Random quantity between 1 and 100 contracts

        # Calculate notional value based on strike price and quantity
        notional_value = strike_price * quantity * 100  # 100 shares per option contract

        # Generate a random trade date at least one year ago
        start_date = datetime.today() - timedelta(days=365 * 3)
        trade_date = start_date + timedelta(days=np.random.randint(0, 365))

        # Calculate initial premium using Black-Scholes model
        T_trade = (expiration_date - trade_date.date()).days / 365  # Time to expiration from trade date in years
        initial_premium = calculate_option_premium_and_greeks(
            S=stock_price,
            K=strike_price,
            T=T_trade,
            r=risk_free_rate,
            sigma=volatility,
            option_type=option_type
        )

        trade_id = str(uuid.uuid4())
        positions.append({
            'trade_id': trade_id,
            'stock': stock,
            'trader': trader,
            'option_type': option_type,
            'strike_price': strike_price,
            'expiration_date': expiration_date,
            'quantity': quantity,
            'direction': direction,
            'notional': notional_value,
            'trade_date': trade_date.date(),
            'initial_premium': initial_premium
        })

    position_data = pd.DataFrame(positions)
    logger.info(position_data)
    return position_data
