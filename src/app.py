import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd

from dash_table.Format import Format, Scheme, Sign, Symbol

import re
import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('DailyStockAverage')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
#app.css.append_css({
#    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
#})


def generate_table(dataframe, max_rows=20):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col],style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'right'}) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def generate_alert_table(dataframe, max_rows=20):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col],style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'right','color': 'red', 'font-weight': 'bold'}) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.layout = html.Div([
    html.H1('Stock Alert'),
    html.H5('Specify the stocks you are interested:'),
    dcc.Input(id='stock-id', value='FB,AMZN,AAPL,GOOG,NK', type='text', style = {'width': '600px'}),  #human text input of stock ticker
    html.Div(id='stock-records', style={'display': 'none'}),
    html.Div(id='valid-ticker'), # Output valid tickers
    html.Hr(),
    html.Div(id='stock-data'),
    html.Hr(),
    html.H5('Specify what percentages to alert you:'),
    dcc.Dropdown(id='perc-dropdown', options=[ {'label':'1%', 'value':'0.01'}, {'label':'2%', 'value':'0.02'}, {'label':'3%', 'value':'0.03'}], value='0.02'),
    html.H5('BE ALERT',style={'color': 'red','font-weight': 'bold'}),
    html.H6('The following stocks in your watchlist are changing rapidly'),
    html.Div(id='stock-alert-data'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
])


# Store selected stock data dataframe in intermediate step.
@app.callback(Output('stock-records', 'children'),
              [Input('stock-id', 'value')])
def query_stock_df(selected_ticker):
    selected_ticker1 = pd.Series(re.split('\W',selected_ticker))
    selected_ticker_upper = [x.upper() for x in selected_ticker1]
    selected_ticker_upper = list( dict.fromkeys(selected_ticker_upper) )
#    df = pd.DataFrame(columns=['Stock', 'TransationTime', 'DailyAveragePrice','Price','TotalVolume','Percentage'])
    df = pd.DataFrame(columns=['Stock', 'TimeNow', 'DailyAveragePrice','Price','TotalVolume','Percentage'])
    for single_ticker in selected_ticker_upper:
        if single_ticker:
            response1 = table.query(KeyConditionExpression=Key('Stock').eq(single_ticker))
            df=df.append(pd.DataFrame.from_dict(response1['Items']), ignore_index=True)
    df = df[['Stock', 'TimeNow', 'DailyAveragePrice','Price','TotalVolume','Percentage']]
    print(df)
    return df.to_json()

# Print the valid tickers.
@app.callback(
    Output('valid-ticker', 'children'),
    [Input('stock-records', 'children')]
)
def print_valid_ticker(df_json):
    valid_ticker = pd.read_json(df_json)['Stock']
    return 'Valid entries: '+', '.join(valid_ticker)

#Print the tables of selected stocks
@app.callback(Output('stock-data', 'children'),
              [Input('stock-records', 'children')])
def plot_stock_df(df_json):
    stock_df = pd.read_json(df_json)
    stock_df['Percentage'] = pd.Series(["{0:.2f}%".format(val * 100) for val in stock_df['Percentage']], index = stock_df.index)
    return generate_table(stock_df)

#Print the tables of stocks with big changes
@app.callback(Output('stock-alert-data', 'children'),
              [Input('stock-records', 'children'),Input('perc-dropdown', 'value')])
def plot_alert_stock_df(df_json, perc):
    stock_alert_df = pd.read_json(df_json)
    percf = float(perc)
    stock_alert_df = stock_alert_df[ stock_alert_df['Percentage'].abs() >percf ]
    stock_alert_df['Percentage'] = pd.Series(["{0:.2f}%".format(val * 100) for val in stock_alert_df['Percentage']], index = stock_alert_df.index)
    return generate_alert_table(stock_alert_df)


if __name__ == '__main__':
    app.run_server(debug=True)
