import os
import json
import urllib.request
import time
from adventofcode_utils.user import User
import operator
from dotenv import load_dotenv

class Leaderboard(object):
    def __init__(self):
        load_dotenv()
        self.sortedUsers = {}
        self.sessid = os.getenv('SESSION_ID')
        self.url = os.getenv('LEADERBOARD_URL')
        self.lastUpdate = 0;

    def get(self):
        #Prevent overloading AoC api
        if(self.lastUpdate != 0):
            if((time.time() - self.lastUpdate) < 900):
                return self.sortedUsers
        
        response = urllib.request.urlopen( urllib.request.Request(self.url, headers = { 'Cookie' : 'session='+self.sessid }) )

        #check if server is alive
        if(response.getcode() != 200):
            return "The site has died, please try again later"

        #checking if cookie hasnt expired
        try:
            variables = json.loads(response.read())
        except ValueError as e:
            return "The Cookie has expired :("

        users = {}
        for x, player in variables["members"].items():
            days = {}

            if player["stars"] > 0:
                for day, stars in player["completion_day_level"].items():
                    days[day] = stars
                for day in range(1, 26):
                    if str(day) not in days.keys():
                        days[str(day)] = ''

            if player["name"] == None:
                player["name"] = "Anonymous"

            users[x] = User(player["name"], player["local_score"], player["global_score"], player["stars"], days)
        
        counter = 0
        for key in sorted(users.values(), key=operator.attrgetter('score'), reverse=True):
            self.sortedUsers[counter] = key
            self.sortedUsers[counter].position = (counter+1)
            counter+=1

        self.lastUpdate = time.time()

        return self.sortedUsers

    def lastUpdate(self):
        return self.lastUpdate