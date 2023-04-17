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
            {'label': 'Vertical Bar', 'value': 'vbar'},
            {'label': 'Horizontal Bar', 'value': 'hbar'}
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
    elif graph_type == 'vbar':
        # Create a vertical bar chart using plotly
        fig = px.bar(df, x='Product', facet_col='Zones', y='Value', color='Metric', barmode='group', facet_row='Indicator')
        # Increase the distance between rows of subplots
        fig.update_layout(height=800)
    elif graph_type == 'hbar':
        # Create a horizontal bar chart using plotly
        fig = px.bar(df, y='Product', facet_col='Zones', x='Value', color='Metric', barmode='group', facet_row='Indicator')
        # Increase the distance between rows of subplots
        fig.update_layout(height=800)
    return fig

# Run the app on a local server
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8080)