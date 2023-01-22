import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
from yahoo_fin import stock_info as si

# Create a sample DataFrame
#df = pd.read_csv('ticker_data.csv')
df = stocklist = si.tickers_sp500()
print(df)
app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='ohlc-graph')
])

@app.callback(Output('ohlc-graph', 'figure'),
              [Input('ticker-dropdown', 'value')])
def update_graph(ticker):
    filtered_df = df[df['ticker'] == ticker]
    trace = go.Ohlc(x=filtered_df['Date'],
                    open=filtered_df['AAPL.Open'],
                    high=filtered_df['AAPL.High'],
                    low=filtered_df['AAPL.Low'],
                    close=filtered_df['AAPL.Close'])
    return {'data': [trace],
            'layout': go.Layout(title=ticker + 'OHLC')}

if __name__ == '__main__':
    app.run_server(debug=True)
