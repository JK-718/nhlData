import requests
import csv

url = "https://statsapi.web.nhl.com/api/v1/game/2017020003/feed/live"
response = requests.get(url)

count = 0

playerId = {}
a = []
b = []

for i in range(2019020001, 2019020002, 1):
    url = 'https://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(i)
    r = requests.get(url)
    gameData = r.json()
    
    for j in ['home', 'away']:
        playerDict = gameData.get('liveData').get('boxscore').get('teams').get(j).get('skaters')
        playerId[j] = playerDict
        
    
    for k in playerId:
        for l in playerId[k]:
            x = gameData.get('liveData').get('boxscore').get('teams').get(k).get('players').get('ID' + str(l)).get('person')
            y = gameData.get('liveData').get('boxscore').get('teams').get(k).get('players').get('ID' + str(l)).get('stats').get('skaterStats')
            a.append(x)
            b.append(y)
            count +=1

with open('pdict.csv', mode='w') as csv_file:
    fieldnames = ['id', 'fullName', 'goals']
    w = csv.DictWriter(csv_file, fieldnames=fieldnames)
    w.writeheader()
    for i in range(count):
        if (b[i]) != None:
            w.writerow({'id': a[i]['id'], 'fullName': a[i]['fullName'], 'goals': b[i]['goals']})

    