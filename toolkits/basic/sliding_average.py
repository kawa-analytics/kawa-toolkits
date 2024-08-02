import datetime
import logging

import pandas as pd
from kywy.client.kawa_decorators import kawa_tool

logger = logging.getLogger('script-logger')

@kawa_tool(
    inputs={
        'measure': float,
        'dimension': str,
        'date': datetime.date,
    },
    outputs={'sliding_average': float},
)
def execute(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(['dimension', 'date'])
    df['sliding_average'] = (df.groupby('dimension')['measure']
                             .rolling(window=10)
                             .mean()
                             .reset_index(level=0, drop=True))
    logger.info(str(df))
    return df


records = []
for day in range(1, 32):
    records.append({
        'date': datetime.date(2020, 1, day),
        'dimension': 'AAPL',
        'measure': 1.1 + day
    })
    records.append({
        'date': datetime.date(2020, 1, day),
        'dimension': 'TSLA',
        'measure': 10.1 + day
    })

a = execute(pd.DataFrame.from_records(records))
...
