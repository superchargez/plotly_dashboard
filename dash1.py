import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
# Load the Excel file into a Pandas dataframe:
df = pd.read_excel('randomdata_1.xlsx', sheet_name=None)

# Create a function to generate a plotly figure for each worksheet:
def generate_figure(df, sheet_name):
    # Filter the dataframe by sheet name
    data = df[sheet_name]
    
    # Create a subplot with 4 rows and 4 columns
    fig = make_subplots(rows=4, cols=4)
    
    # Loop through each product and performance indicator
    for i, product in enumerate(['PSTN', 'BB', 'FF', 'IPTV']):
        for j, indicator in enumerate(['MTTR', 'repeat', 'denial', 'refusal']):
            # Calculate the row and column indices for the subplot
            row = j + 1
            col = i + 1
            
            # Add a bar chart to the subplot
            fig.add_trace(
                go.Bar(x=data['Zones'], y=data[product + '_' + indicator + '_Curr']),
                row=row, col=col
            )
            
            # Add a line for the target, last month, and last year values
            fig.add_trace(
                go.Scatter(x=data['Zones'], y=data[product + '_' + indicator + '_Target'], mode='lines', name='Target'),
                row=row, col=col
            )
            fig.add_trace(
                go.Scatter(x=data['Zones'], y=data[product + '_' + indicator + '_LM'], mode='lines', name='Last Month'),
                row=row, col=col
            )
            fig.add_trace(
                go.Scatter(x=data['Zones'], y=data[product + '_' + indicator + '_LY'], mode='lines', name='Last Year'),
                row=row, col=col
            )
            
            # Set the title and axis labels for the subplot
            fig.update_layout(title=sheet_name + ': ' + product + ' - ' + indicator)
            fig.update_xaxes(title_text='Zone', row=row, col=col)
            fig.update_yaxes(title_text=indicator, row=row, col=col)
    
    return fig

# Loop through each worksheet and generate a plotly figure:
figures = []
for sheet_name in df.keys():
    figures.append(generate_figure(df, sheet_name))

#Combine the plotly figures into a single dashboard:
dashboard = make_subplots(rows=4, cols=4)
for i, fig in enumerate(figures):
    row = (i // 4) + 1
    col = (i % 4) + 1
    for trace in fig['data']:
        dashboard.add_trace(trace, row=row, col=col)
    dashboard.update_layout(title='Dashboard')
