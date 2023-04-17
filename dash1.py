import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px

# Read data from CSV file
df = pd.read_csv('data256.csv')

# Create a sunburst chart using plotly
fig = px.sunburst(df, path=['Zones', 'Indicator', 'Product', 'Metric'], values='Value')

# Create a dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Run the app on a local server
if __name__ == '__main__':
    # app.run_server(debug=True, port=8080)
    app.run_server(debug=True, host="0.0.0.0", port=8080)