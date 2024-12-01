import requests
import os
import json
import time
from models import User, Day
import operator
from dotenv import load_dotenv


class AoCAPI(object):
    sortedUsers: list[User]
    session_id: str
    url: str
    lastUpdate: float

    def __init__(self):
        load_dotenv()
        self.sortedUsers = []
        self.lastUpdate = 0

        session_id = os.getenv('SESSION_ID')
        url = os.getenv('LEADERBOARD_URL')
        if session_id is None or url is None:
            print("ERROR: Session cookie or leaderboard URL is missing")
            quit()

        self.session_id = session_id
        self.url = url

    def get_leaderboard(self) -> list[User]:
        # Prevent overloading AoC api
        if (self.lastUpdate != 0):
            if ((time.time() - self.lastUpdate) < 900):
                return self.sortedUsers

        headers = {
            "Cookie": f"session={self.session_id}"
        }
        response = requests.get(self.url, headers=headers)

        # check if server is alive
        if (response.status_code != 200):
            raise LeaderboardError(
                "AoC API responded with non-200 status code")

        # checking if cookie hasnt expired
        if (response.url != self.url):
            # We have been redirected
            raise LeaderboardError(
                "AoC API responded with redirect. Check session cookie.")

        response_data = response.json()

        # Build the users list from the retrieved data
        users: list[User] = []
        for _, player in response_data["members"].items():
            days = {}

            # Set name to anonymous of not set
            if player["name"] == None:
                player["name"] = "Anonymous"

            for day in range(1, 26):
                day_obj: Day
                if str(day) in player["completion_day_level"]:
                    day_stars = player["completion_day_level"][str(day)]
                    day_obj = Day(
                        day_stars["1"]["get_star_ts"] if "1" in day_stars else None,
                        day_stars["2"]["get_star_ts"] if "2" in day_stars else None,
                    )
                else:
                    day_obj = Day(None, None)
                days[day] = day_obj

            users.append(User(player["name"], player["local_score"],
                         player["global_score"], player["stars"], days))

        # Sort the users list
        users.sort(key=lambda x: x.localScore, reverse=True)

        # Set leaderboard positions in User objects
        for i in range(len(users)):
            users[i].leaderboard_position = i + 1 # 0th index is 1st on the leaderboard

        self.sortedUsers = users
        self.lastUpdate = time.time()

        return self.sortedUsers


class LeaderboardError(Exception):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message
