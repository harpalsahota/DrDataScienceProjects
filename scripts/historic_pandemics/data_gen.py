import re
import json

import pandas as pd

df = pd.read_csv('./pandemic_list.csv', header=0)
df = df[['Location', 'Date', 'Disease']]

r = re.compile('[0-9]+')


points = []
manual_updates = {
    0: {'Location': 'Central Asia, Mesopotamia and Southern Asia', 'Disease': 'Unknown, possibly Flu'},
    1: {'Location': 'Greece, Libya, Egypt, Ethiopia'},
    10: {'Location': 'Europe', 'Disease': 'Unknown, possibly hantavirus'},
    22: {'Location': 'Southern New England', 'Disease': 'Unknown, many possible explanations'},
    218: {'Location': 'Worldwide'},
}
for row_index, row in enumerate(df.itertuples()):
    years = r.findall(row.Date)
    if not all(len(x) == len(years[0]) for x in years):
        full, partial = sorted(years, key=len, reverse=True)
        diff = len(full) - len(partial)
        years = [full, f'{full[:diff]}{partial}']
    years = [int(i) for i in years]
    data_point = {
        'XMin': min(years),
        'XMax': max(years),
        'Y': row_index,
        'Location': row.Location,
        'Disease': row.Disease.strip('.')
    }
    if 'BC' in row.Date:
        years = [-int(i) for i in years]
        data_point.update({'XMin': min(years), 'XMax': max(years),})
    if 'present' in row.Date:
        data_point['XMax'] = 'present'
    if row_index in manual_updates:
        data_point.update(manual_updates[row_index])
    points.append(data_point)

with open('pandemic_list.json', 'w') as out:
    json.dump(points, out)