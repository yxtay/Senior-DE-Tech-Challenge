from pathlib import Path

from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import requests


DATA_URL = "https://api.covid19api.com/country/singapore/status/confirmed"
DATA_PARQUET = "covid.parquet"

def get_data():
    if Path(DATA_PARQUET).exists():
        return pd.read_parquet(DATA_PARQUET)
    
    response = requests.get(DATA_URL)
    df = pd.DataFrame(response.json())
    df["Date"] = pd.to_datetime(df["Date"])
    df.to_parquet(DATA_PARQUET)
    return df

df = get_data()
start_date = df["Date"].min()
end_data = df["Date"].max()

app = Dash(__name__)
app.layout = html.Div([
    html.H1(children='COVID19 cases in Singapore over time', style={'textAlign':'center'}),
    dcc.DatePickerRange(
        id='date-picker-range',
        display_format='DD-MM-YYYY',
        min_date_allowed=start_date,
        max_date_allowed=end_data,
        start_date=start_date,
        end_date=end_data
    ),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
)
def update_graph(start_date, end_date):
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    return px.line(df[mask], x='Date', y='Cases')

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
