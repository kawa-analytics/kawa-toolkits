import datetime
import pandas as pd
from kywy.client.kawa_decorators import kawa_tool


@kawa_tool(
    inputs={
        'measure': float,
        'dimension': str,
        'date': datetime.date,
    },
    outputs={'sliding_average': float},
)
def execute(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values('date')
    df['sliding_average'] = (df.groupby('dimension')['measure']
                             .rolling(window=10)
                             .mean()
                             .reset_index(level=0, drop=True))
    return df
