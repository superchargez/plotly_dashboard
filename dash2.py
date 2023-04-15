import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data from the Excel file
df = pd.read_excel('randomdata_1.xlsx')

# Define the dimensions of the data
num_zones = 4
num_products = 4
num_indicators = 4

# Create a figure with a 4x4 grid of subplots
fig, axes = plt.subplots(num_indicators, num_products, figsize=(16, 16))

# Loop through each product and performance indicator
for i in range(num_products):
    for j in range(num_indicators):
        # Select the data for the current product and performance indicator
        data = df[(df['Product'] == 'Product {}'.format(i+1)) & (df['Indicator'] == 'Indicator {}'.format(j+1))]
        
        # Create a bar plot for the current product and performance indicator
        sns.barplot(x='Zones', y='Curr', data=data, ax=axes[j, i])
        
        # Add labels to the plot
        axes[j, i].set_title('Product {} - Indicator {}'.format(i+1, j+1))
        axes[j, i].set_xlabel('')
        axes[j, i].set_ylabel('')
        
        # Add a horizontal line for the target value
        target = data.iloc[0]['Target']
        axes[j, i].axhline(y=target, color='r', linestyle='--')
        
        # Add a legend to the plot
        handles, labels = axes[j, i].get_legend_handles_labels()
        axes[j, i].legend(handles, ['Current Month', 'Target'])
        
# Add a title to the figure
fig.suptitle('Performance Dashboard')

