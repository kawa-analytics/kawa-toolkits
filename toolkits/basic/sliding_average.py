from datetime import date
import pandas as pd
from kywy.client.kawa_decorators import kawa_tool
import unittest


@kawa_tool(
    inputs={'measure': float, 'dimension': str, 'date': date},
    outputs={'sliding_average': float},
    parameters={'window': {'type': float, 'default': 10}}
)
def execute(df: pd.DataFrame, window) -> pd.DataFrame:
    df = df.sort_values(['dimension', 'date'])
    df['sliding_average'] = (df.groupby('dimension')['measure']
                             .rolling(window=window)
                             .mean()
                             .reset_index(level=0, drop=True))

    df.fillna(0, inplace=True)
    return df


class TestSlidingAverage(unittest.TestCase):
    def test_area(self):
        num = 10
        window = 4
        df = execute(
            df=pd.DataFrame({
                'date': [date(2025, 1, i) for i in range(1, num)],
                'measure': range(1, num),
                'dimension': [f'd{i%2}' for i in range(1, num)],
            }),
            window=window
        )

        self.assertEqual(
            first=df['sliding_average'].tolist(),
            second=[0, 0, 0, 5, 0, 0, 0, 4, 6],
        )


if __name__ == '__main__':
    unittest.main()