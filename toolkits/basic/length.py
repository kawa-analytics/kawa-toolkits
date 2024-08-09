import logging
import pandas as pd
from kywy.client.kawa_decorators import kawa_tool

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={'text': str},
    outputs={'length': float},
)
def main(df: pd.DataFrame) -> pd.DataFrame:
    logger.info('Starting the execution')
    logger.info(df)
    df['length'] = df['text'].apply(lambda x: len(x))
    return df
