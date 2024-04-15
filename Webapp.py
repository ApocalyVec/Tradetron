import logging
import threading
from multiprocessing import Process

from flask import Flask
import dash
from dash import html, dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from multiprocessing import Process, Manager


from src.front_end.MeowTrade import MeowTrade

app = Flask(__name__)
dash_app = dash.Dash(__name__, server=app, routes_pathname_prefix='/dash/')

# Initialize the DataFrame with a few initial data points
manager = Manager()
data_list = manager.list()
# df = pd.DataFrame(columns=['Time', 'Value'])

# Define the layout of the Dash app
dash_app.layout = html.Div([
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    ),
])


# Callback to update the graph
@dash_app.callback(
    Output('live-graph', 'figure'),
    Input('graph-update', 'n_intervals')
)
def update_graph_scatter(n):
    if len(data_list) > 0:
        temp_df = pd.DataFrame(list(data_list))
        logging.info(f"Frontend: Updating graph with {len(data_list)} data points with the latest price {data_list[-1]}")
        return {
            'data': [go.Scatter(
                x=temp_df['Time'],
                y=temp_df['Value'],
                name='Scatter',
                mode='lines+markers'
            )],
            'layout': go.Layout(
                xaxis=dict(title='Time', range=[min(temp_df['Time']), max(temp_df['Time'])]),
                yaxis=dict(title='Price', range=[min(temp_df['Value']), max(temp_df['Value'])]),
                title='Streaming SPY Price',
            )
        }

@app.route('/')
def home():
    return 'Navigate to "/dash" to see the live graph!'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Start Tradetron in a separate process
    tradetron_process = Process(target=lambda: MeowTrade(data_list=data_list).setup_connection())
    tradetron_process.start()

    app.run(debug=True)
