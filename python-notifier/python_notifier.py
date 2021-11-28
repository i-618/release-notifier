import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import glob
import os


r = requests.get('https://www.python.org/downloads/')
soup = BeautifulSoup(r.text, 'html.parser')


ver_list = soup.find_all('div', {'class':'row download-list-widget'})[0]
ver_list = ver_list.ol.find_all('li')
ver_list[0]


classes_text = ['release-number', 'release-date']
classes_link = ['release-download', 'release-enhancements']
list_vers_parsed = []
for rel in ver_list:
    item = {}
    for key in classes_link:
        item[key] = rel.find('span', class_=key).a.attrs['href']
    for key in classes_text:
        item[key] = rel.find('span', class_=key).text
    list_vers_parsed.append(item)




list_of_files = glob.glob('./*.json') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)



with open(latest_file) as r:
    release_num = json.load(r)[0]['release-number']


for i, d in enumerate(list_vers_parsed):
    if release_num in d.values():
        index = i
        break

if index == 0:
    print('We are in the latest version')
else:
    print(f'We are behind by {index} versions')
    print(f'''
##############################################
versions releases are {list_vers_parsed[0: index]}
##############################################
    ''')
    today = datetime.today().strftime("%d-%b-%Y")
    with open(f'py-ver-hist-{today}.json', 'w') as f:
        json.dump(list_vers_parsed, f, indent=4)





