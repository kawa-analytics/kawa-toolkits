import logging
import pandas as pd
from kywy.client.kawa_decorators import outputs, inputs

logger = logging.getLogger('script-logger')


@inputs(text=str)
@outputs(length=float)
def execute(df: pd.DataFrame):
    logger.info('Starting the execution')
    df['length'] = df.apply(lambda row: len(row['text']), axis=1)
    return df
