import pandas as pd
from kywy.client.kawa_decorators import kawa_tool
from slack_sdk import WebClient


@kawa_tool(
    inputs={'dimension': str, 'metric': float, },
    secrets={'channel': 'slack_channel', 'token': 'slack_token', },
)
def execute(df: pd.DataFrame, channel: str, token: str) -> pd.DataFrame:
    num_rows = len(df)
    table = df.head(20).to_markdown()
    note = f'(Showing 20 rows out of {num_rows})' if num_rows > 20 else ''
    send_to_slack(
        channel=channel,
        token=token,
        message=f'Here is your data {note}:\n```{table}```')


def send_to_slack(channel: str, token: str, message: str):
    client = WebClient(token=token)
    client.chat_postMessage(
        channel=channel,
        text=message
    )

