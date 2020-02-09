import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import re
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('DailyStockAverage')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

def get_color(a):
    if a%2 == 0:
        return "#A0DCF6"
    else:
        return "#E9F5FB"

def generate_table(dataframe, max_rows=20):
    return html.Table(
        # Header
        [html.Tr([
            html.Th(col) for col in dataframe.columns
            ])
        ] +

        # Body
        [html.Tr([
            html.Td(
                dataframe.iloc[i][col],
                style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'right', 'backgroundColor': get_color(i)}
            ) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def generate_alert_table(dataframe, max_rows=20):
    return html.Table(
        # Header
        [html.Tr([
            html.Th(col) for col in dataframe.columns
            ])
        ] +

        # Body
        [html.Tr([
            html.Td(
                dataframe.iloc[i][col],
                style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'right','color': 'red', 'font-weight': 'bold'}
            ) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

# Store selected stock data dataframe in intermediate step.
@app.callback(Output('stock-records', 'children'),
             [Input('stock-ticker', 'value'),Input('interval-component','n_intervals')])
def query_stock_df(selected_ticker,n):
    selected_ticker1 = pd.Series(re.split('\W',selected_ticker))
    selected_ticker_upper = [x.upper() for x in selected_ticker1]
    selected_ticker_upper = list( dict.fromkeys(selected_ticker_upper) )
    df = pd.DataFrame(columns=['Stock', 'TransactTime', 'DailyAveragePrice','Price','TotalVolume','Percentage'])
    for single_ticker in selected_ticker_upper:
        if single_ticker:
            response1 = table.query(KeyConditionExpression=Key('Stock').eq(single_ticker))
            df=df.append(pd.DataFrame.from_dict(response1['Items']), ignore_index=True)
    df = df[['Stock', 'TransactTime', 'DailyAveragePrice','Price','TotalVolume','Percentage']]
    return df.to_json()

# Print the valid tickers.
@app.callback(Output('valid-ticker', 'children'),
              [Input('stock-records', 'children')]
             )
def print_valid_ticker(df_json):
    valid_ticker = pd.read_json(df_json)['Stock']
    return ', '.join(valid_ticker)

#Print the tables of selected stocks
@app.callback(Output('stock-data', 'children'),
              [Input('stock-records', 'children')]
             )
def plot_stock_df(df_json):
    stock_df = pd.read_json(df_json)
    stock_df['Percentage'] = pd.Series(["{0:.2f}%".format(val * 100) for val in stock_df['Percentage']], index = stock_df.index)
    print(datetime.datetime.now())
    return generate_table(stock_df)

#Print the tables of stocks with big changes
@app.callback(Output('stock-alert-data', 'children'),
              [Input('stock-records', 'children'),Input('perc-dropdown', 'value')]
             )
def plot_alert_stock_df(df_json, perc):
    stock_alert_df = pd.read_json(df_json)
    percf = float(perc)
    stock_alert_df = stock_alert_df[ stock_alert_df['Percentage'].abs() >percf ]
    stock_alert_df['Percentage'] = pd.Series(["{0:.2f}%".format(val * 100) for val in stock_alert_df['Percentage']], index = stock_alert_df.index)
    return generate_alert_table(stock_alert_df)

# Layout
app.layout = html.Div(
        [
            html.Img(
                id='logo', src=app.get_asset_url("SA.jpg"),
                style = {'width': '100px', 'height': '100px', 'display': 'inline-block'}
            ),
            html.H2(
                'Stock Alert',
                style={'color': 'blue', 'font-weight': 'bold','display': 'inline-block', 'position': 'absolute', 'margin': '40px 0'}
            ),
            html.H6(
                '— No crash you are not aware of',
                style={'color': 'blue','font-weight': 'bold', 'padding-top':'2px'}
            ),
            html.Hr(),
            html.Div(
                [
                    html.H6('Specify the stocks you are interested in:'),
                    dcc.Input(
                        id='stock-ticker', value='FB,AMZN,AAPL,GOOG,NK,O,Z', type='text',
                        style = {'width': '600px', 'backgroundColor': '#E8E8E8' }
                    ),  #human text input of stock ticker
                    html.Div(id='stock-records', style={'display': 'none'}),
                    html.H5('Valid entries',style={'color': 'blue','font-weight': 'bold'}),
                    html.Div(id='valid-ticker'), # Output valid tickers
                    html.Div(id='stock-data'),
                    html.Hr(),
                ],
                style={'width':'50%', 'height':'100%','float':'left'}
            ),
            html.Div(
                [
                    html.H6('Specify the percentage to alert you:'),
                    dcc.Dropdown(
                        id='perc-dropdown',
                        options=[ {'label':'1%', 'value':'0.01'}, {'label':'2%', 'value':'0.02'},
                            {'label':'3%', 'value':'0.03'}, {'label':'5%', 'value':'0.05'}, {'label':'10%', 'value':'0.1'}],
                        value='0.02',
                        style = {'backgroundColor': '#E8E8E8' }
                    ),
                    html.H5('ALERT',style={'color': 'red','font-weight': 'bold'}),
                    html.Div('The following stocks in your watchlist are changing rapidly:'),
                    html.Div(id='stock-alert-data')
                ],
                style={'width':'50%', 'height':'100%','float':'left'}
            ),
            dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
            )
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True,port='8080',host="ec2-52-87-24-57.compute-1.amazonaws.com")
