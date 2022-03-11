import math
import season

class Model:
    def __init__(self, matches, teams):
        self.matches = matches
        self.teams = teams

    def estimate_probability(self, blue, orange, time):
        pass

    def update(self, match):
        pass



class ELO(Model):
    def __init__(self, matches, teams, model_path):
        self.matches = matches
        #self.events = events
        self.path = model_path
        self.ratings = dict()
        self.count = dict()
        self.names = dict()

        for team in teams:
            id = team.id
            name = team.name
            self.ratings[id] = 0
            self.names[id] = name
            self.count[id] = 0

        for match in matches:
            self.update(match)

    def update(self, match):
        orange_id = match.orange.id
        orange_game_count = self.count[orange_id]
        blue_id = match.blue.id
        blue_game_count = self.count[blue_id]
        diff = 0.01 * (self.ratings[orange_id] - self.ratings[blue_id])
        blue_gain = 10 / (math.e**(-diff) + 1)
        orange_gain = 10 / (math.e **(diff) + 1)

        blue_win_count = match.score[0]
        orange_win_count = match.score[1]

        self.ratings[blue_id] = self.ratings[blue_id] + (blue_win_count * blue_gain
        - orange_win_count * orange_gain) * (1 + 9 * math.e ** (-blue_game_count))
        self.ratings[orange_id] = self.ratings[orange_id] + (orange_win_count * orange_gain
        - blue_win_count * blue_gain) * (1 + 9 * math.e ** (-orange_game_count))
        self.count[blue_id] = blue_game_count + blue_win_count + orange_win_count
        self.count[orange_id] = orange_game_count + blue_win_count + orange_win_count

    def log(self, path):
        labels = ['id', 'name', 'games played', 'rating']
        dataList = [[], [], [], []]
        for id in ratings.keys():
            rating = ratings[id]





if __name__ == '__main__':
    rlcsx_na = season.Season('data/rlcsx/NA')
    print(f'{len(rlcsx_na.events)} events')
    print(f'{len(rlcsx_na.matches)} matches')
    print(f'{len(rlcsx_na.teams)} teams')


    estimate = Model(rlcsx_na.matches, rlcsx_na.teams, None)

    rlcsx_na.teams.sort(key = (lambda x : estimate.ratings[x.id]))




    for team in rlcsx_na.teams:
        print(f'{team.name} : {estimate.ratings[team.id]} : {estimate.count[team.id]}')
