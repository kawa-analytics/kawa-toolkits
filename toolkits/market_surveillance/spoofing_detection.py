import datetime

import numpy as np

from kywy.client.kawa_decorators import kawa_tool
from datetime import date, datetime
import logging
import pandas as pd

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={
        'order_id': str,
        'order_date_time': datetime,
        'order_cancellation_time': datetime,
        'order_size': float,
        'order_status': str,
    },
    outputs={
        'spoof_detected': bool
    },
)
def spoofing_detection(df):
    order_book = df
    logger.info('Starting spoofing detection')
    logger.info(df)

    # Convert Order Time and Cancellation Time to datetime
    order_book['order_date_time'] = pd.to_datetime(order_book['order_date_time'])
    order_book['order_cancellation_time'] = pd.to_datetime(order_book['order_cancellation_time'], errors='coerce')

    # Initialize the spoof detection column to False
    order_book['spoof_detected'] = False

    # Filter for large orders (using a threshold, e.g., 900 shares)
    large_orders = order_book[order_book['order_size'] > 900].copy()

    # Calculate time differences for canceled orders
    large_orders['Time Difference'] = (
            large_orders['order_cancellation_time'] - large_orders['order_date_time']).dt.total_seconds()

    # Identify orders that are canceled shortly after being placed (e.g., within 30 seconds)
    large_orders['Spoof Detected'] = (large_orders['order_status'] == 'Canceled') & (
            large_orders['Time Difference'] <= 30)

    # Create a result DataFrame with Order ID and Spoof Detected status
    output = large_orders[['order_id', 'Spoof Detected']]

    logger.info('Spoofing detection is done')
    logger.info(output)

    return output