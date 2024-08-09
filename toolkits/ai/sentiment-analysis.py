import logging

import pandas as pd
from gender_detector.gender_detector import GenderDetector
from kywy.client.kawa_decorators import kawa_tool
from textblob import TextBlob

logger = logging.getLogger('script-logger')


@kawa_tool(
    inputs={'text': str},
    outputs={'sentiment': str},
)
def execute(df: pd.DataFrame) -> pd.DataFrame:
    df['sentiment'] = df['text'].apply(lambda x: analyze_sentiment(x))
    logger.info(df)
    return df


def analyze_sentiment(text: str) -> str:
    blob = TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity
    if sentiment_polarity > 0:
        return "Positive"
    elif sentiment_polarity < 0:
        return "Negative"
    else:
        return "Neutral"
