import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv('data256.csv')

app.layout = html.Div([
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Sunburst', 'value': 'sunburst'},
            {'label': 'Barplot', 'value': 'barplot'}
        ],
        value='sunburst'
    ),
    dcc.Dropdown(
        id='zone',
        options=[{'label': i, 'value': i} for i in df['Zones'].unique()],
        value='National'
    ),
    dcc.Graph(id='indicator-graph')
])

@app.callback(
    Output('zone', 'style'),
    Input('graph-type', 'value'))
def toggle_zone_dropdown(graph_type):
    if graph_type == 'sunburst':
        return {'display': 'none'}
    else:
        return {'display': 'block'}

@app.callback(
    Output('indicator-graph', 'figure'),
    Input('graph-type', 'value'),
    Input('zone', 'value'))
def update_graph(graph_type, zone):
    if graph_type == 'sunburst':
        fig = px.sunburst(df, path=['Zones', 'Product', 'Indicator', 'Metric'], values='Value')
    else:
        dff = df[df['Zones'] == zone]
        fig = px.bar(dff, x='Product', y='Value', color='Metric', barmode='group', facet_row='Indicator')
        fig.update_layout(height=800)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8080)