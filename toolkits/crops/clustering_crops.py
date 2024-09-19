from sklearn.cluster import KMeans
import pandas as pd
from kywy.client.kawa_decorators import kawa_tool

@kawa_tool(
    inputs={
        'Rainfall_mm': float,
        'Temperature_C': float,
        'Fertilizer_Usage_kg_per_hectare': float,
        'Crop_Yield_tons_per_hectare': float
    },
    outputs={
        'Cluster': str,
    },
)
def perform_clustering(df):

    # Predefined features for clustering
    cluster_features = ['Rainfall_mm', 'Temperature_C', 'Fertilizer_Usage_kg_per_hectare', 'Crop_Yield_tons_per_hectare']
    
    # Ensure the required features are in the DataFrame
    if not all(feature in df.columns for feature in cluster_features):
        missing_features = [feature for feature in cluster_features if feature not in df.columns]
        raise ValueError(f"The following features are missing from the DataFrame: {missing_features}")
    
    # Number of clusters and random state
    n_clusters = 5
    random_state = 42
    
    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    df['Cluster'] = kmeans.fit_predict(df[cluster_features])

    return df
