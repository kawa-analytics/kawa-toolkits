import datetime
import logging

import pandas as pd
import numpy as np
from time import time
from kywy.client.kawa_decorators import kawa_tool
from sklearn.ensemble import IsolationForest
from geopy.distance import geodesic

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={
        'client_id': float,
        'amount': float,
        'date': datetime.datetime,
        'location_lat': float,
        'location_long': float,
    },
    outputs={
        'is_point_anomaly': bool,
        'is_behavioral_anomaly': bool,
        'is_spatial_anomaly': bool,
    }
)
def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Start the process")
    start_time = time()
    for client_id, group in df.groupby('client_id'):
        logger.info(f'Now working in client={client_id}')
        df.loc[group.index, 'is_point_anomaly'] = detect_point_anomalies(group)
        df.loc[group.index, 'is_behavioral_anomaly'] = detect_behavioral_anomalies(group)
        df.loc[group.index, 'is_spatial_anomaly'] = detect_spatial_anomalies(group)

    end_time = time()
    seconds_elapsed = end_time - start_time
    logger.info(f"Computation is done in {seconds_elapsed}s")
    return df


def detect_point_anomalies(transactions_for_one_client):
    group = transactions_for_one_client.copy()
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    group['anomaly_score'] = model.fit_predict(group[['amount']])
    return group['anomaly_score'] == -1


def detect_behavioral_anomalies(transactions_for_one_client, threshold=2.8):
    group = transactions_for_one_client.copy()
    group.sort_values(by=['date'], inplace=True)
    group['rolling_mean'] = group['amount'].rolling(window=10, min_periods=1).mean()
    group['rolling_std'] = group['amount'].rolling(window=10, min_periods=1).std()

    return np.abs(group['amount'] - group['rolling_mean']) > (threshold * group['rolling_std'])


def detect_spatial_anomalies(transactions_for_one_client, threshold_in_kilometers=5000):
    group = transactions_for_one_client.copy()
    group.sort_values(by=['date'], inplace=True)
    group['prev_lat'] = group['location_lat'].shift(1)
    group['prev_long'] = group['location_long'].shift(1)

    group['distance_from_prev'] = group.apply(lambda row: geodesic(
        (row['location_lat'], row['location_long']),
        (row['prev_lat'], row['prev_long'])
    ).kilometers if pd.notnull(row['prev_lat']) else 0, axis=1)

    return group['distance_from_prev'] > threshold_in_kilometers
