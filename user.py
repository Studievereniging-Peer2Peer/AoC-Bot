class User(object):
    def __init__(self, name, score, globalScore, stars, days):
        self.name = name
        self.score = score
        self.globalScore = globalScore
        self.stars = stars
        self.days = days
        self.position = -1