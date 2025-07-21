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
    def test_with_window_greater_than_one(self):
        # given
        window = 4

        # when
        df = execute(df=self.gen_test_data(), window=window)

        # then
        self.assertEqual(
            first=df['sliding_average'].tolist(),
            second=[0, 0, 0, 5, 0, 0, 0, 4, 6],
        )

    def test_with_window_equals_to_one(self):
        # given
        window = 1

        # when
        df = execute(df=self.gen_test_data(), window=window)

        # then
        self.assertEqual(
            first=df['sliding_average'].tolist(),
            second=[2, 4, 6, 8, 1, 3, 5, 7, 9],
        )

    @staticmethod
    def gen_test_data():
        return pd.DataFrame({
            'date': [date(2025, 1, i) for i in range(1, 10)],
            'measure': range(1, 10),
            'dimension': [f'd{i%2}' for i in range(1, 10)],
        })


if __name__ == '__main__':
    unittest.main()
