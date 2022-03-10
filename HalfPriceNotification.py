#Send a message the day after Jake Guetzel scores
import praw #reddit api
import datetime
import requests #allows HTTP requests
import json #reading json

#reddit API setup
reddit = praw.Reddit('bot1') #create reddit instance based on bot info in praw.ini
redditor = reddit.redditor('usernameHere') #add recipient username

#general setup to use the Stats API
prefix = 'https://statsapi.web.nhl.com/api/v1/' #prefix for URLs
myTeam = 'Pittsburgh Penguins' #team of interst, id=5
myTeamId = '5' #penguins ID

today = datetime.date.today() #get today's date
yesterday = today - datetime.timedelta(days=1) #get yesterday's date
# yesterday = datetime.date(2021,12,14)
# today = datetime.date(2021,12,15)

myPlayerId = 8477404 #Jake's player id
# myPlayerId = 8470619 #test player
fullPlayerId = 'ID{}'.format(myPlayerId)

#get player info
urlStrPlayer = '{}people/{}'.format(prefix,myPlayerId) #format player url
jOutPlayer = requests.get(urlStrPlayer).json() #get JSON output from url
myPlayer = jOutPlayer['people'][0]['fullName'] #get player name

#compile schedule URL
urlStrSched = '{}schedule?teamId={}&startDate={}&endDate={}'.format(prefix,myTeamId,yesterday,today) #combine elements to get url
jOutSched = requests.get(urlStrSched).json() #get JSON output from url
#check if there's a finished game from the day before
gameStatus = jOutSched['dates'][0]['games'][0]['status']['abstractGameState'] #get game status (final or not)
if gameStatus == 'Final': #set game ID if game was completed
    gameId = jOutSched['dates'][0]['games'][0]['gamePk'] #get game ID 
else:  #print error message if game isn't in 'final' status
    output = 'Game Status = {}'.format(gameStatus)
    print(output)
    exit() #if not a final game, quit

#compile game URL
urlStrGame = ('{}game/{}/boxscore').format(prefix,gameId) #'formula' to combine elements for gameinto url
jOutGame = requests.get(urlStrGame).json() #get JSON output for game
gamePlayers = jOutGame['teams']['home']['players'] #get to the point in the JSON when we can specify a player

#result based on player score
if fullPlayerId in gamePlayers: #if player is in JSON, they played that game
    playerGoals = gamePlayers[fullPlayerId]['stats']['skaterStats']['goals'] #if player played, check goals scored
else:
    output = '{} did not play'.format(myPlayer)
    print(output)
    exit()

if playerGoals>0:
    output = 'Milkshakes half off today: {}. \nThanks, {}'.format(today,myPlayer)
    # print(output)
else:
    output = 'No milkshakes for you! {} \nThanks for nothing, {}'.format(today,myPlayer)
    # print(output)

#message information
subject='Milkshakes!' #subject for message
message=output #body for message

redditor.message(subject,message) #send the message
