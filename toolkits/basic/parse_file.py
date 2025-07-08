import datetime

import pandas as pd
from kywy.client.kawa_decorators import kawa_tool


@kawa_tool(
    inputs={'id': str},
    outputs={'content': str},
    parameters={'upload': { 'extensions': ['txt'] }}
)
def execute(df: pd.DataFrame, upload: str) -> pd.DataFrame:
    # Stores the content of the uploaded file into the 'content' column of the output df
    with open(upload, 'r') as file:
        content = file.read()
        
    df['content'] = content
        
    return df
