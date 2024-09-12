import logging
import pandas as pd
from kywy.client.kawa_decorators import kawa_tool

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={'Units Sold': float, 'total_days': float, 'product_leadtime_mapping': float},
    outputs={'Reorder Point': float}
)
def compute_reorder_point(df):
    # Define the fixed safety stock
    safety_stock = 10
    df['Average Daily Usage'] = df['Units Sold'] / df['total_days']
    df['Reorder Point'] = (df['Average Daily Usage'] * df['product_leadtime_mapping']) + safety_stock
    return df
