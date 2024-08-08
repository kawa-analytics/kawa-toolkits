import pandas as pd
from gender_detector.gender_detector import GenderDetector
from kywy.client.kawa_decorators import kawa_tool


@kawa_tool(
    inputs={'first_name': str},
    outputs={'gender': str},
)
def execute(df: pd.DataFrame) -> pd.DataFrame:
    detector = GenderDetector('us')
    df['gender'] = df['first_name'].apply(lambda x: detector.guess(x))
    return df
