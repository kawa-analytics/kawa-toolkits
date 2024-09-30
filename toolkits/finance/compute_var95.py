import numpy as np

from kywy.client.kawa_decorators import kawa_tool
from datetime import date
import logging

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={'stock': str, 'date': date, 'price':float},
    outputs={'var95': float},
)
def calculate_var_95(df):

    df = df.sort_values(by='date')
    df['return'] = df.groupby('stock')['price'].pct_change()
    df = df.dropna(subset=['return'])

    var_95 = df.groupby('stock')['return'].apply(lambda x: np.percentile(x, 5)).reset_index()
    var_95.columns = ['stock', 'var95']

    df = df.merge(var_95, on='stock', how='left')
    logger.info(df)
    df = df.drop(columns=['return'])

    return df
