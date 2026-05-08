import random
import datetime
import pandas as pd

from kywy.client.kawa_decorators import kawa_tool


@kawa_tool(
    outputs={
        'id': str,
        'name': str,
        'amount': float,
        'category': str,
        'created_at': datetime.date,
    },
)
def run():
    categories = ['alpha', 'beta', 'gamma', 'delta']
    today = datetime.date.today()
    rows = []
    for i in range(50):
        rows.append({
            'id': f'foo-{i:04d}',
            'name': f'Item {i}',
            'amount': round(random.uniform(10, 1000), 2),
            'category': random.choice(categories),
            'created_at': today - datetime.timedelta(days=random.randint(0, 90)),
        })
    return pd.DataFrame(rows)
