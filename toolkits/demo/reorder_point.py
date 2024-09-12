import logging
import pandas as pd
import datetime
from kywy.client.kawa_decorators import kawa_tool

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={'units_sold': float, 'transaction_date': datetime.date, 'product_leadtime': float, 'product_name': str},
    outputs={'Reorder Point': float}
)
def compute_reorder_point(df):
    # Define the fixed safety stock
    safety_stock = 10
    
    aggregated = df.groupby(by=['product_name']).agg(
    min_date=('transaction_date', 'min'),
    max_date=('transaction_date', 'max'),
    total_sold=('units_sold', 'sum')).reset_index()

    # Merge the original DataFrame with the aggregated DataFrame
    df_merged = pd.merge(df, aggregated, on='product_name', how='left')

    # Compute the total days between min and max transaction date per product
    df_merged['total_days'] = df_merged.apply(lambda row: (row['max_date'] - row['min_date']).days, axis=1)
    
    df['Average Daily Usage'] = df['total_sold'] / df['total_days']
    df['Reorder Point'] = (df['Average Daily Usage'] * df['product_leadtime']) + safety_stock
    return df
