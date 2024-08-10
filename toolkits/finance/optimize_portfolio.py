import pandas as pd
from kywy.client.kawa_decorators import kawa_tool
import logging
from kywy.client.kawa_client import KawaClient as K
import numpy as np
from scipy.optimize import minimize

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={'Ticker': str, 'holdings': float, 'last_price': float},
    outputs={'Weight': float, 'Optimized_Holdings': float},
)
def execute(df: pd.DataFrame, kawa):
    returns = load_returns(kawa)

    # Calculate expected returns and covariance matrix
    expected_returns = returns.mean() * 252  # annualize the returns
    cov_matrix = returns.cov() * 252  # annualize the covariance

    # Number of assets
    tickers = returns.columns
    num_assets = len(tickers)

    # Objective function (negative Sharpe Ratio)
    def sharpe_ratio(weights):
        portfolio_return = np.dot(weights, expected_returns)
        portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -(portfolio_return / portfolio_stddev)  # negative because we minimize

    # Constraints: Sum of weights is 1 and at least 2 assets in the portfolio
    def portfolio_constraints(weights):
        return np.sum(weights) - 1  # sum of weights must be 1

    # Bounds for each weight: between 0 and 1
    bounds = [(0, 1) for _ in range(num_assets)]

    # Additional constraints to ensure at least two tickers in the portfolio
    def at_least_two_tickers(weights):
        return np.sum(weights > 0.01) - 2  # at least two weights must be greater than 0.01

    constraints = (
        {'type': 'eq', 'fun': portfolio_constraints},
        {'type': 'ineq', 'fun': at_least_two_tickers}
    )

    # Initial guess (equally distributed weights)
    initial_weights = np.ones(num_assets) / num_assets

    # Optimization
    result = minimize(sharpe_ratio, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    optimal_weights = result.x

    # Calculate total portfolio value
    total_value = (df['holdings'] * df['last_price']).sum()

    # Create a dataframe for the optimal portfolio
    portfolio = pd.DataFrame({
        'Ticker': tickers,
        'Weight': optimal_weights
    })

    # Display the optimal portfolio
    logger.info(portfolio)
    df = df.merge(portfolio, on='Ticker', how='left')

    # Calculate optimized holdings
    df['Optimized_Holdings'] = (df['Weight'].fillna(0) * total_value / df['last_price']).round().astype(int)

    logger.info(df)
    return df


def load_returns(kawa):
    """
    Loads market data from a kawa sheet
    """
    load_market_data_from_sheet = 'Ptf - Ticker histo'
    histo_df = (kawa
                .sheet(sheet_name=load_market_data_from_sheet)
                .select(K.col('Date'), K.col('Ticker'), K.col('Close'))
                .no_limit()
                .compute())
    histo_df = histo_df.sort_values(by=['Ticker', 'Date'])
    histo_df['returns'] = histo_df.groupby('Ticker')['Close'].pct_change()
    return histo_df.pivot(index='Date', columns='Ticker', values='returns').dropna()
