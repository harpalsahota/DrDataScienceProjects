import json

import pandas as pd

df = pd.read_csv('path\to\csv', delimiter=',', header=0)

female_df = df[(df['Variable'] == 'Females at birth') & (df['Measure'] == 'Years')]
male_df = df[(df['Variable'] == 'Males at birth') & (df['Measure'] == 'Years')]

merged_df = pd.merge(female_df, male_df, how='inner', on=['COU', 'Year'], suffixes=('_female', '_male'))
merged_df = merged_df[['COU', 'Year', 'Value_female', 'Value_male']]

merged_df['life_diff'] = merged_df['Value_female'] - merged_df['Value_male']

min_year = merged_df['Year'].min()
max_year = merged_df['Year'].max()


countries = sorted(merged_df['COU'].unique())

grouped_by_year = merged_df.groupby(by='Year')

all_data = []
previous_years = {}
counts = {}
for year, group in grouped_by_year:
    year_data = {'year': year, 'data': []}
    for country in countries:
        life_diff = list(group[group['COU'] == country]['life_diff'])
        if life_diff:
            previous_years[country] = life_diff[0]
            year_data['data'].append({'country': country, 'life_diff': life_diff[0]})
        else:
            if country not in previous_years:
                previous_years[country] = 0
            counts[country] = counts.get(country, 0) + 1
            year_data['data'].append({'country': country, 'life_diff': previous_years[country]})
    all_data.append(year_data)


with open('life_expectancy_difference.json', 'w') as out_json:
    json.dump({'data': all_data}, out_json)

print(sorted(counts.items(), key=lambda x: x[1], reverse=True))