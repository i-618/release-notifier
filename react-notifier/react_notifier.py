import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import glob
import os


r = requests.get('https://reactjs.org/versions/')
soup = BeautifulSoup(r.text, 'html.parser')


ver_list = soup.find_all('div', class_="css-15weewl")[0]
ver_list = ver_list.find_all('div')




list_vers_parsed = []
for rel in ver_list:
    item = {}
    item['release-number'] = rel.h3.text
    item['change-log'] = rel.ul.li.a.attrs['href']
    list_vers_parsed.append(item)




list_of_files = glob.glob('./*.json')
if len(list_of_files) == 0:
    index = 1
else:
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
    with open(f'react-ver-hist-{today}.json', 'w') as f:
        json.dump(list_vers_parsed, f, indent=4)





