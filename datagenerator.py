import pandas as pd
import numpy as np

# generate random data
# Define the dimensions of the data
num_zones = 4
num_products = 4
num_indicators = 4

# Create a dictionary to store the data
data = {}

# Loop through each zone, product, and performance indicator
for i in range(num_zones):
    zone_name = 'Zone ' + str(i+1)
    data[zone_name] = {}
    for j in range(num_products):
        product_name = 'Product ' + str(j+1)
        data[zone_name][product_name] = {}
        for k in range(num_indicators):
            indicator_name = 'Indicator ' + str(k+1)
            data[zone_name][product_name][indicator_name] = {}
            
            # Generate random data for current month, target, last month, and last year
            data[zone_name][product_name][indicator_name]['Curr'] = np.random.randint(0, 100, 1)[0]
            data[zone_name][product_name][indicator_name]['Target'] = np.random.randint(0, 100, 1)[0]
            data[zone_name][product_name][indicator_name]['LM'] = np.random.randint(0, 100, 1)[0]
            data[zone_name][product_name][indicator_name]['LY'] = np.random.randint(0, 100, 1)[0]

#Convert the dictionary to a Pandas dataframe:
# Convert the dictionary to a dataframe
df = pd.DataFrame.from_dict({(i,j,k): data[i][j][k]
                             for i in data.keys()
                             for j in data[i].keys()
                             for k in data[i][j].keys()},
                            orient='index')

# Reset the index and rename the columns
df = df.reset_index().rename(columns={'level_0': 'Zone', 'level_1': 'Product', 'level_2': 'Indicator', 'level_3': 'Value'})

# Save the dataframe to an Excel file
df.to_excel('randomdata.xlsx', index=False)
