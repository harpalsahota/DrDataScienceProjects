
import json

import requests
from bs4 import BeautifulSoup
from iso3166 import countries

COUNTRY_MAPPING = {
    'United Kingdom': 'UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND',
    'United States': 'UNITED STATES OF AMERICA'
}

response = requests.get('https://en.wikipedia.org/wiki/List_of_Formula_One_World_Drivers%27_Champions')
html_doc = response.content
soup = BeautifulSoup(html_doc, 'html.parser')

# index one currently the By season table
champions = []
table = soup.find_all('table')[1]
rows = table.find_all('tr')
for r in rows[1:]:
    cells = r.find_all('td')
    try:
        season = cells[0].find('a').text.strip()
        driver_anchors = cells[1].find_all('a')
        nationality = driver_anchors[0].get('title')
        driver = driver_anchors[1].get('title')
        driver = {
            'season': season,
            'nationality': nationality,
            'champion': driver,
        }
        try:
            driver['country_code'] =  countries.get(nationality).alpha2.lower()
        except KeyError:
            driver['country_code'] = countries.get(COUNTRY_MAPPING[nationality]).alpha2.lower()
        champions.append(driver)
    except (IndexError, AttributeError):
        pass

with open('f1_world_champions_by_nationality.json', 'w') as out_file:
    json.dump(champions, out_file)

