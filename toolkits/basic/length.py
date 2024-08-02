import logging
import pandas as pd
from kywy.client.kawa_decorators import kawa_tool

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={
        'text': str,
    },
    outputs={
        'length': float,
    }
)
def execute(df: pd.DataFrame):
    logger.info('Starting the execution')
    df['length'] = df.apply(lambda row: len(row['text']), axis=1)
    return df
