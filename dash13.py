from plotly.subplots import make_subplots
import math, dash
from dash.dependencies import Input, Output
from dash import dcc, html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

file = "data256.csv"
df = pd.read_csv(file)

dropdown = dcc.Dropdown(
    id='chart-type',
    options=[
        {'label': 'Treemap', 'value': 'treemap'},
        {'label': 'Parallel Categories', 'value': 'parallel_categories'},
        {'label': 'Image', 'value': 'image'},
        {'label': 'Sunburst', 'value': 'sunburst'},
        {'label': 'Barplot', 'value': 'barplot'}
    ],
    value='treemap'
)

graph = dcc.Graph(id='graph')

back_button = html.Button(
    id='back-button',
    children='Back',
    n_clicks=0,
    style={'display': 'none'}  # Initially hidden
)

zone_dropdown = dcc.Dropdown(
    id='zone-dropdown',
    options=[{'label': zone, 'value': zone} for zone in df['Zones'].unique()],
    value=df['Zones'].iloc[0]
)

heatmap_dropdown = dcc.Dropdown(
    id='heatmap-dropdown',
    options=[
        {'label': 'Zone', 'value': 'Zones'},
        {'label': 'Product', 'value': 'Product'},
        {'label': 'Indicator', 'value': 'Indicator'}
    ],
    value='Zones'
)

app.layout = html.Div([
    dropdown,
    zone_dropdown,
    heatmap_dropdown,
    graph,
    back_button
])

@app.callback(
    Output('graph', 'figure'),
    Input('chart-type', 'value'),
    Input('zone-dropdown', 'value'),
    Input('heatmap-dropdown', 'value'),
    Input('back-button', 'n_clicks')
)

def update_graph(chart_type, zone, heatmap_type, n_clicks):
    if chart_type == 'treemap':
        fig1 = px.treemap(df, path=['Zones', 'Product', 'Indicator', 'Metric'], values='Value', custom_data=['Value'])
        fig1.update_traces(texttemplate='%{label}<br>%{customdata[0]}')
        if n_clicks > 0:
            fig1 = px.treemap(df, path=['Zones', 'Product', 'Indicator', 'Metric'], values='Value')
        return fig1
    elif chart_type == 'sunburst':
        fig2 = px.sunburst(df, path=['Zones', 'Product', 'Indicator', 'Metric'], values='Value', custom_data=['Value'])
        fig2.update_traces(texttemplate='<b>%{label}</b> <span style="font-size: 16px;"><span style="font-size: 16px;">%{customdata[0]}</span></b><br>%{currentPath}</span>')
        return fig2
    elif chart_type == 'parallel_categories':
        fig3 = px.parallel_categories(df, dimensions=['Zones', 'Product', 'Indicator', 'Metric'], color='Value')
        return fig3
    elif chart_type == 'image':
        unique_values = df[heatmap_type].unique()
        num_values = len(unique_values)
        cols = 2
        rows = math.ceil(num_values / cols)

        fig4 = make_subplots(rows=rows, cols=cols, subplot_titles=unique_values)

        for i, value in enumerate(unique_values):
            dff = df[df[heatmap_type] == value]
            if heatmap_type == 'Zones':
                heatmap = px.imshow(dff.pivot_table(index='Product', columns='Indicator', values='Value'))
            elif heatmap_type == 'Product':
                heatmap = px.imshow(dff.pivot_table(index='Zones', columns='Indicator', values='Value'))
            else:
                heatmap = px.imshow(dff.pivot_table(index='Zones', columns='Product', values='Value'))
            fig4.add_trace(heatmap.data[0], row=(i // cols) + 1, col=(i % cols) + 1)
        fig4.update_layout(title=f'Heatmaps by {heatmap_type}', height=800)
        return fig4
    elif chart_type == 'barplot':
        dff = df[df['Zones'] == zone]
        fig = px.bar(dff, x='Product', y='Value', color='Metric', barmode='group', facet_row='Indicator')
        product_labels = dff["Product"].unique()
        threshold = 92  # Set a threshold value for the bars.  This is the value for the "ideal" bar.  It will be halfway between the top of the "actual" bar and
        for i, indicator in enumerate(dff["Indicator"].unique()[::-1]):
            fig.update_yaxes(title_text=indicator, row=i + 1, col=1, tickangle=0)
            for j, metric in enumerate(dff["Metric"].unique()):
                values = dff[(dff["Indicator"] == indicator) & (dff["Metric"] == metric)]['Value']
                textposition = ['inside' if value >= threshold else 'outside' for value in values]
                fig.update_traces(
                    text=values.astype(str),
                    textposition=textposition,

                    textfont_color=['white' if pos == 'inside' else 'black' for pos in textposition],
                    row=i + 1,
                    col=1,
                    selector=dict(legendgroup=metric)
                )


        fig.update_layout(
       height=800,
        xaxis=dict(
        title=None,

        showticklabels=False
                ),
            xaxis4=dict(
            side='top',
            showticklabels=True,
            title=dict(text='Product')
                    )
            )
        
    return fig

@app.callback(
    Output('back-button', 'style'),
    Input('chart-type', 'value')
)
def update_visibility(chart_type):
    if chart_type in ('treemap', 'sunburst'):
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output('zone-dropdown', 'style'),
    Input('chart-type', 'value')
)
def update_zone_dropdown_visibility(chart_type):
    if chart_type == 'barplot':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output('heatmap-dropdown', 'style'),
    Input('chart-type', 'value')
)
def update_heatmap_dropdown_visibility(chart_type):
    if chart_type == 'image':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

if __name__ == '__main__':
    app.run_server(debug=True, port=8013)
