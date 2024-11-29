import logging
import pandas as pd
from kywy.client.kawa_decorators import kawa_tool

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={'text': str},
    outputs={'length': float, 'length3': float},
)
def main(df: pd.DataFrame) -> pd.DataFrame:
    logger.info('Starting the execution now')
    logger.info(df)
    df['length'] = df['text'].apply(lambda x: len(x))
    df['length2'] = df['text'].apply(lambda x: len(x))
    return df
