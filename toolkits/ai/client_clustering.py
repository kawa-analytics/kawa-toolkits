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
        'cluster_name': str,
        'cluster_description': str
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
    n_clusters = 4
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)  # Adjust n_clusters as needed
    df['cluster'] = kmeans.fit_predict(normalized_features)

    # Calculate cluster centroids
    centroids = kmeans.cluster_centers_

    # Generate cluster names and descriptions
    cluster_names = {i: f"Cluster{i + 1}" for i in range(n_clusters)}
    cluster_descriptions = {}
    for i, centroid in enumerate(centroids):
        description = (f"Total: {centroid[1]:.2f}, "
                       f"Avg: {centroid[0]:.2f}, "
                       f"Min: {centroid[2]:.2f}, "
                       f"Max: {centroid[3]:.2f}, "
                       f"StdDev: {centroid[4]:.2f}, "
                       f"Transactions: {centroid[5]:.2f}")
        cluster_descriptions[i] = description

    df['cluster_name'] = df['cluster'].map(cluster_names)
    df['cluster_description'] = df['cluster'].map(cluster_descriptions)

    # Generate the output DataFrame with client_id and cluster_name
    output_df = df[['client_id', 'cluster_name', 'cluster_description']]
    logger.info(f'Output df: {output_df}')
    return output_df
