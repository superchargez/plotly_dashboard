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
        fig = px.sunburst(df, path=['Zones', 'Product', 'Indicator', 'Metric'], values='Value', custom_data=['Value'])
        # fig.update_traces(texttemplate='%{label} (%{parent})<br>%{customdata[0]}')
        fig.update_traces(texttemplate='<b>%{label}</b> <span style="font-size: 14px;"><b><span style="font-size: 16px;">%{customdata[0]}</span></b><br>%{currentPath}</span>')
        # fig.update_traces(texttemplate='%{label}<br>%{currentPath}<br>%{customdata[0]}')
        
    else:
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

if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.1", port=8012)