import datetime
import pandas as pd
from kywy.client.kawa_decorators import kawa_tool


@kawa_tool(
    inputs={'measure': float, 'date': datetime.date},
    outputs={'sliding_average': float},
)
def execute(df: pd.DataFrame) -> pd.DataFrame:
    df['sliding_average'] = df['measure'].rolling(window=10).mean()
    return df
