import logging

import pandas as pd
from gender_detector.gender_detector import GenderDetector
from kywy.client.kawa_decorators import kawa_tool

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={'first_name': str},
    outputs={'gender': str},
)
def execute(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(str(df))
    detector = GenderDetector('us')
    df['gender'] = 'OK'
    return df

