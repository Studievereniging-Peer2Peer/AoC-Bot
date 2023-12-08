import datetime
from string import Formatter
from models import User



def timeTaken(startTime, endTime):
    difference = datetime.datetime.fromtimestamp(endTime) - datetime.datetime.fromtimestamp(startTime)
    return difference

def timeTakenFormatted(startTime, endTime):
    difference = datetime.datetime.fromtimestamp(endTime) - datetime.datetime.fromtimestamp(startTime)

    # Thanks to mpounsett https://stackoverflow.com/questions/8906926/formatting-timedelta-objects
    fmt = "**{D}** days **{H}** hrs **{M}** mins **{S}** secs"
    f = Formatter()
    d = {}
    l = {'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
    k = map(lambda x: x[1], list(f.parse(fmt)))
    rem = int(difference.total_seconds())

    for i in ('D', 'H', 'M', 'S'):
        if i in k and i in l.keys():
            d[i], rem = divmod(rem, l[i])

    return f.format(fmt, **d)

def timeDeltaFormatted(startTime, endTime):
    difference = endTime - startTime

    # Thanks to mpounsett https://stackoverflow.com/questions/8906926/formatting-timedelta-objects
    fmt = "**{D}** days **{H}** hrs **{M}** mins **{S}** secs"
    f = Formatter()
    d = {}
    l = {'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
    k = map(lambda x: x[1], list(f.parse(fmt)))
    rem = int(difference.total_seconds())

    for i in ('D', 'H', 'M', 'S'):
        if i in k and i in l.keys():
            d[i], rem = divmod(rem, l[i])

    return f.format(fmt, **d)

def getUserFromLeaderboard(leaderboard: list[User], username: str) -> User | None:
    for user in leaderboard:
        if user.name.lower() == username.lower():
            return user
    return None
