import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import glob
import os


r = requests.get('https://pandas.pydata.org/docs/whatsnew/index.html')
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')




ver_list = soup.find('section', id="release-notes")
ver_list = ver_list.find_all('li', class_="toctree-l1")



list_vers_parsed = []
for rel in ver_list:
    item = {}
    ver_date = rel.find_all('a')[0].text.replace(')','').replace('What’s new in', 'Version').split('(')
    item['release-number'] = ver_date[0]
    item['date-released'] = ver_date[1]
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
    with open(f'pandas-ver-hist-{today}.json', 'w', encoding='utf-8') as f:
        json.dump(list_vers_parsed, f, indent=4, ensure_ascii=False)





