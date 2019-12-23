import requests
import json
import matplotlib.pyplot as plt
import csv


url = "https://statsapi.web.nhl.com/api/v1/game/2017020003/feed/live"
response = requests.get(url)


data = response.text
parsed = json.loads(data)

#Enter team name for shots in a given range
teamVar = str(input())
shotx, shoty = [], []

#set the range of games to scrape shot data from
#uses the NHL's gamePK identifier
#can extend or shrink the amount of games, and change the time frame
for i in range(2019020001, 2019020220, 1):
    urlBig = 'https://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(i)
    r = requests.get(urlBig)
    gameData = r.json()
     
    plays = gameData.get('liveData').get('plays').get('allPlays')
    players = gameData.get('liveData').get
    for i in plays:
        if 'team' in i:
            name = (i['team']['name'])
            #Caps used as an example, to use different team simply enter entire name in line 30 here
            #No other changes necessary
            if name == teamVar and i['result']['event'] == 'Shot':
                #Bring all shots to one side of the rink
                x = abs(i['coordinates']['x'])
                y = i['coordinates']['y']
                home = gameData.get('gameData').get('teams').get('home').get('name')
                period = i['about']['period']
                #Normalizing for which end teams shoot on
                #Necessary because of the absolute value for x shots
                if (name == home and period %2 != 0) or (name != home and period%2 == 0):
                    shotx.append(x)
                    shoty.append(y)
                else:
                    y = -y
                    shotx.append(x)
                    shoty.append(y)
                    
        
#graphics
plt.scatter(shotx, shoty)
plt.show()
plt.hist2d(shotx, shoty, bins = 15)
plt.show()


#Writes data to file, can be opened with SQL to add to database or by R to run stats or graphics
with open('file.csv', mode='w') as csv_file:
    fieldnames = ['shots - x', 'shots - y']
    w = csv.DictWriter(csv_file, fieldnames=fieldnames)
    w.writeheader()
    for i,j in zip(shotx, shoty):
        w.writerow({'shots - x': i, 'shots - y': j})
       
