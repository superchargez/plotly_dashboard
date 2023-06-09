import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px

# Read data from CSV file
df = pd.read_csv('data256.csv')

# Create a dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    # Add a drop-down menu for selecting the graph type
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Sunburst', 'value': 'sunburst'},
            {'label': 'Bar', 'value': 'bar'},
            {'label': 'Scatter', 'value': 'scatter'},
            {'label': 'Line', 'value': 'line'}
        ],
        value='sunburst'
    ),
    # Add a container for displaying the selected graph
    dcc.Graph(id='graph')
])

# Define a callback function to update the displayed graph
@app.callback(
    Output('graph', 'figure'),
    [Input('graph-type', 'value')]
)
def update_graph(graph_type):
    if graph_type == 'sunburst':
        # Create a sunburst chart using plotly
        fig = px.sunburst(df, path=['Zones', 'Indicator', 'Product', 'Metric'], values='Value')
    elif graph_type == 'bar':
        # Create a bar chart using plotly
        fig = px.bar(df, x='Product', facet_col='Zones', y='Value', color='Metric', barmode='group', facet_row='Indicator')
    elif graph_type == 'scatter':
        # Create a scatter chart using plotly
        fig = px.scatter(df, x='Product', facet_col='Zones', y='Value', color='Metric', facet_row='Indicator')
    elif graph_type == 'line':
        # Create a line chart using plotly
        fig = px.line(df, x='Product', facet_col='Zones', y='Value', color='Metric', facet_row='Indicator')
    return fig

# Run the app on a local server
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8080)