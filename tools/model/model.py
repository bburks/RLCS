import trueskill as ts
import pandas as pd
from ..formats import format as ft
from ..data.requester import load

class Model:
    def __init__(self, loading_folder = None):
        self.ratings = dict()
        self.rater = ts.TrueSkill(draw_probability = 0)

    def get_rating(self, team):
        try:
            res = self.ratings[team]
        except:
            res = self.rater.create_rating()
        finally:
            return res

    def set_rating(self, team, rating):
        self.ratings[team] = rating

    def game_odds(self, t1, t2):
        r1 = self.get_rating(team)
        r2 = self.get_rating(team)

        delta_mu = t1.mu - t2.mu
        sum_sigma = t1.sigma ** 2 + t2.sigma ** 2
        denom = math.sqrt(2 * (BETA * BETA) + sum_sigma)
        ts = rater
        return ts.cdf(delta_mu / denom)

    def update_ratings(self, game):
        t1 = game.get_blue()
        t2 = game.get_orange()
        if game.get_winner() == t1:
            winner = t1
            loser = t2
        elif game.get_winner() == t2:
            winner = t2
            loser = t1
        else:
            assert False, 'game needs to be completed'

        r1, r2 = self.rater.rate_1vs1(self.get_rating(winner), self.get_rating(loser))
        self.set_rating(winner, r1)
        self.set_rating(loser, r2)

    def save(self, folder, name = 'ratings'):
        data = []
        for id in self.ratings:
            data.append({'id' : id, 'mu': self.ratings[id].mu, 'sigma': self.ratings[id].sigma})
        df = pd.DataFrame(data)
        df['lower_bound'] = df['mu'] - 2 * df['sigma']
        df = df.sort_values('lower_bound', ascending = False)
        df.drop('lower_bound', axis = 1, inplace = True)
        df = df.reset_index(drop = True)
        df.to_csv(f'{folder}/{name}.csv')

def evaluate(matches, games):
    model = Model()
    for row in games.iterrows():
        game = get_game(matches, row)
        model.update_ratings(game)

def get_game(matches, game_row):
    match_id = game_row['match']
    match_row = matches.loc[match_id, :]
    blue_id = match_row['blue_id']
    orange_id = match_row['orange_id']
    blue_name = match_row['blue_name']
    orange_name = match_row['orange_name']
    blue = ft.Team(id = blue_id, name = blue_name)
    orange = ft.Team(id = orange_id, name = orange_name)
    blue_won = game_row['blue'] > game_row['orange']
    if blue_won:
        game = ft.Game(blue = blue, orange = orange, winner = blue)
    else:
        game = ft.Game(blue = blue, orange = orange, winner = orange)
    return game

def get_games(matches, games):
    gamerator = []
    for index, game_row in games.iterrows():
        gamerator.append(get_game(matches, game_row))
    return gamerator

def _get_region(events, matches, match_id):
    event_id = matches.loc[match_id, 'event']
    region = events.loc[event_id, 'region']
    return region

def evaluate_region(region, path):

    events = load(path = path, type = 'events')
    matches = load(path = path, type = 'matches')
    games = load(path = path, type = 'games')
    region_events = events.loc[events['region'] == region]
    region_event_ids = region_events.index
    region_matches = matches.loc[matches['event'].isin(region_event_ids)]
    region_match_ids = region_matches.index
    region_games = games.loc[games['match'].isin(region_match_ids)]
    model = Model()
    gamerator = get_games(matches, region_games)
    for game in gamerator:
        model.update_ratings(game)
    model.save(path, name = f'ratings_{region}')
