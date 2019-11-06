import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import pyodbc
import csv


url = "https://statsapi.web.nhl.com/api/v1/game/2017020003/feed/live"
response = requests.get(url)


data = response.text
parsed = json.loads(data)

shotx, shoty = [], []


for i in range(2019020001, 2019020220, 1):
    urlBig = 'https://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(i)
    r = requests.get(urlBig)
    gameData = r.json()
     
    plays = gameData.get('liveData').get('plays').get('allPlays')
    players = gameData.get('liveData').get
    for i in plays:
        if 'team' in i:
            name = (i['team']['name'])
            if name == 'Washington Capitals' and i['result']['event'] == 'Shot':
                x = abs(i['coordinates']['x'])
                y = i['coordinates']['y']
                home = gameData.get('gameData').get('teams').get('home').get('name')
                period = i['about']['period']
                if (name == home and period %2 != 0) or (name != home and period%2 == 0):
                    shotx.append(x)
                    shoty.append(y)
                else:
                    y = -y
                    shotx.append(x)
                    shoty.append(y)
        
       
plt.scatter(shotx, shoty)
plt.show()
plt.hist2d(shotx, shoty, bins = 15)
plt.show()



with open('file.csv', mode='w') as csv_file:
    fieldnames = ['shots - x', 'shots - y']
    w = csv.DictWriter(csv_file, fieldnames=fieldnames)
    w.writeheader()
    for i,j in zip(shotx, shoty):
        w.writerow({'shots - x': i, 'shots - y': j})
       