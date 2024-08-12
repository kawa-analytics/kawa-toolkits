import logging

import pandas as pd
from kywy.client.kawa_decorators import kawa_tool
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={
        'client_id': float,
        'total_transaction_amount': float,
        'avg_transaction_amount': float,
        'min_transaction_amount': float,
        'max_transaction_amount': float,
        'stddev_transaction_amount': float,
        'num_transactions': float,
    },
    outputs={
        'cluster': float
    },
)
def execute(df: pd.DataFrame) -> pd.DataFrame:
    # Features for clustering, including the number of transactions
    features = df[[
        'avg_transaction_amount',
        'total_transaction_amount',
        'min_transaction_amount',
        'max_transaction_amount',
        'stddev_transaction_amount',
        'num_transactions']]

    logger.info(f'Feature df: {features}')

    # Normalize the features
    scaler = StandardScaler()
    normalized_features = scaler.fit_transform(features)

    # Apply KMeans Clustering
    kmeans = KMeans(n_clusters=4, random_state=42)  # Adjust n_clusters as needed
    df['cluster'] = kmeans.fit_predict(normalized_features)

    # Calculate cluster centroids
    centroids = kmeans.cluster_centers_

    # Generate unique cluster names based on total transaction amount
    sorted_centroids = sorted(enumerate(centroids), key=lambda x: x[1][1])  # Sort by total_transaction_amount
    cluster_names = {
        idx: f"Cluster {i + 1} - {('High' if i == len(sorted_centroids) - 1 else 'Low')} Total Transaction Amount"
        for i, (idx, _) in enumerate(sorted_centroids)}

    df['cluster_name'] = df['cluster'].map(cluster_names)

    # Generate the output DataFrame with client_id and cluster_name
    output_df = df[['client_id', 'cluster_name']]
    logger.info(f'Output df: {output_df}')
    return output_df
