"""
Script to process data for Oil and Gas wells post
https://www.drdatascience.co.uk/portfolio/oil-and-gas-wells
"""
import json

import pandas as pd

df = pd.read_csv(
    'path/to/csv',
    header=0,
    encoding='latin1'
)

df = df[['CURRENT_STATUS', 'WATER_DEPTH', 'ORIG_SURF_X_LONG', 'ORIG_SURF_Y_LAT', 'WELL_PRODUCT']]

df = df.dropna(axis=0, how='any')

status_mapping = {
    'DRILLING': 'Drilling',
    'COMPLETED_OPERATING': 'Operating',
    'COMPLETED_SHUT_IN': 'Plugged',
    'PLUGGED': 'Plugged',
    'AB1': 'Abandoned',
    'AB2': 'Abandoned',
    'AB3': 'Abandoned',
}

well_product_mapping = {
    'GAS': 'Gas',
    'OIL': 'Oil',
    'WATER': 'Water',
    'GAS, OIL': 'Gas & Oil',
    'CONDENSATE, GAS': 'Gas',
    'CONDENSATE, OIL': 'Oil',
    'CONDENSATE, GAS, OIL': 'Gas & Oil',
    'CONDENSATE': 'Unknown',
    'CONDENSATE, GAS, WATER': 'Gas & Water'
}

df = df.replace({'CURRENT_STATUS': status_mapping})
df = df.replace({'WELL_PRODUCT': well_product_mapping})

df = df[df['WELL_PRODUCT'] != 'Unknown']
df = df[df['WELL_PRODUCT'] != 'Gas & Water']
df = df[df['WELL_PRODUCT'] != 'Gas & Oil']


df = df.sort_values(['ORIG_SURF_Y_LAT', 'ORIG_SURF_X_LONG'], ascending=[0, 0])

json_data = []
for row in df.iterrows():
    row_index, row_data = row
    json_data.append(row_data.to_dict())

with open('oil_and_gas_data.json', 'w') as out_json:
    json.dump({'data': json_data}, out_json)
