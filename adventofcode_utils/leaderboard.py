import os
import json
import urllib.request
import time
from adventofcode_utils.user import User
import operator

class Leaderboard(object):
    def __init__(self):
        self.sortedUsers = {}
        self.sessid = "53616c7465645f5f9cc1d3ca6f068cc4ee74c0d0fb614cb510e07801c0c9ada2d56e6f9397745b9e742b4d5334caa052"
        self.url = "https://adventofcode.com/2021/leaderboard/private/view/959961.json"
        self.lastUpdate = 0;

    def get(self):
        users = {}
        # #checking if 15 minutes from previous request has already passed
        # #its important because we dont want to cause issues to the creator of AoC!!!!
        if(self.lastUpdate != 0):
            if((time.time() - self.lastUpdate) < 900):
                return self.users
        
        #getting the json of your leaderboards
        response = urllib.request.urlopen( urllib.request.Request(self.url, headers = { 'Cookie' : 'session='+self.sessid }) )
        #check if server is alive
        if(response.getcode() != 200):
            return "The site has died, please try again later"
        #checking if cookie hasnt expired, they tend to expire after around a month so putting a fresh one on the start of december should last until the end
        try:
            variables = json.loads(response.read())
        except ValueError as e:
            return "The Cookie has expired :("

        for x, player in variables["members"].items():
            data = {}

            if player["stars"] > 0:
                for day, stars in player["completion_day_level"].items():
                    data[day] = len(stars)

            users[x] = User(player["name"], player["local_score"], player["stars"], data)
        
        counter = 0
        for key in sorted(users.values(), key=operator.attrgetter('score'), reverse=True):
            self.sortedUsers[counter] = key
            counter+=1

        self.lastUpdate = time.time()

        return self.sortedUsers

    def lastUpdate(self):
        return self.lastUpdate