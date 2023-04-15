import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Define the app
app = dash.Dash(__name__)

# Load the data from the Excel file
df = pd.read_excel('randomdata_1.xlsx')

# Define the dropdown options
dropdown_options = [
    {"label": "Product 1", "value": "Product 1"},
    {"label": "Product 2", "value": "Product 2"},
    {"label": "Product 3", "value": "Product 3"},
    {"label": "Product 4", "value": "Product 4"},
]

# Define the app layout
app.layout = html.Div(
    [
        # Define the dropdown
        dcc.Dropdown(
            id="product-dropdown",
            options=dropdown_options,
            value="Product 1",
        ),
        
        # Define the graphs
        html.Div(
            [
                dcc.Graph(id="curr-graph"),
                dcc.Graph(id="target-graph"),
                dcc.Graph(id="lm-graph"),
                dcc.Graph(id="ly-graph"),
            ],
            className="row",
        ),
    ]
)


# Define the callback to update the graphs
@app.callback(
    [
        Output("curr-graph", "figure"),
        Output("target-graph", "figure"),
        Output("lm-graph", "figure"),
        Output("ly-graph", "figure"),
    ],
    [Input("product-dropdown", "value")],
)
def update_graphs(product):
    # Filter the data for the selected product
    filtered_df = df[df["Product"] == product]

    # Create the figures for each indicator
    curr_fig = px.bar(filtered_df, x="Zones", y="Curr", color="Indicator", barmode="group")
    target_fig = px.bar(filtered_df, x="Zones", y="Target", color="Indicator", barmode="group")
    lm_fig = px.bar(filtered_df, x="Zones", y="LM", color="Indicator", barmode="group")
    ly_fig = px.bar(filtered_df, x="Zones", y="LY", color="Indicator", barmode="group")

    # Return the figures
    return curr_fig, target_fig, lm_fig, ly_fig


if __name__ == "__main__":
    app.run_server(debug=True)
