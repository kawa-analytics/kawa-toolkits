import pandas as pd
from kywy.client.kawa_decorators import kawa_tool
from slack_sdk import WebClient


@kawa_tool(
    inputs={'dimension': str, 'metric': float, },
    outputs={},
    secrets={'channel': 'slack_channel', 'token': 'slack_token', },
)
def execute(df: pd.DataFrame, channel: str, token: str) -> pd.DataFrame:
    send_to_slack(
        channel=channel,
        token=token,
        message='Hi')


def send_to_slack(channel: str, token: str, message: str):
    client = WebClient(token=token)
    client.chat_postMessage(
        channel=channel,
        text=message
    )
