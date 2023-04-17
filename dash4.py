import pandas as pd
import plotly.express as px
from plotly.offline import plot

# Read data from CSV file
df = pd.read_csv('data256.csv')

# Reshape data into long format
# df_melted = df.melt(id_vars=['Zones', 'Product', 'Indicator'], var_name='Metric', value_name='Value')

# Create a dashboard using plotly
fig = px.bar(df, x='Product', facet_col='Zones', y='Value', color='Metric', barmode='group', facet_row='Indicator')

# Save the plot as an HTML file and open it in the web browser
plot(fig, filename='dashboard.html')