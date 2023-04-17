import pandas as pd
import plotly.express as px
from plotly.offline import plot

# Read data from CSV file
df = pd.read_csv('data256.csv')

# Create a sunburst chart using plotly
fig = px.sunburst(df, path=['Zones', 'Indicator', 'Product', 'Metric'], values='Value')

# Save the plot as an HTML file and open it in the web browser
plot(fig, filename='dashboard.html')