import logging
import pandas as pd
from kywy.client.kawa_decorators import kawa_tool

logger = logging.getLogger('script-logger')


@kawa_tool(inputs={'product_name': str, 'discount': float})
def main(df: pd.DataFrame) -> pd.DataFrame:
    logger.info('Will publish the following data on the website')
    logger.info(df)
    df['length'] = df['text'].apply(lambda x: len(x))
    return df


def update_website(df):
    path_to_html_file = '/home/kawa/website/index.html'

    html_rows = []
    for index, row in df.iterrows():
        if row['discount'] > 0:
            product_name = row['product_name']
            discount = str(row['discount']) + '% Off'
            html_rows.append(f'''
            <li>
                <span class="product">{product_name}</span>
                <span class="discount"><nobr>{discount}</nobr></span>
            </li>''')

    html_content = '\n'.join(html_rows)

    with open(path_to_html_file, 'w') as html:
        html.write(f'''
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Wayne Enterprises Tech Product Discounts!</title>
                <link rel="stylesheet" href="style.css">
            </head>
            <body>
                <div class="container">
                    <h1>Wayne Enterprises discounted products</h1>
                    <ul class="products">{html_content}</ul>
                </div>
            </body>
            </html>''')
