from ..formats import format
import trueskill
import pandas as pd
import math
from random import random

BETA = 4.166666666666667
rater = trueskill.TrueSkill(draw_probability = 0, tau = 8.333, beta = BETA)


def make_first_to_odds(teams, ratings, first_to, sim_count):
    list = []
    ids = ratings.index
    for t1 in ids:

        odds = dict()
        name1 = teams.loc[t1, 'name']
        odds['winner'] = name1
        team1 = format.Team(id = t1, name = name1)
        print(f'starting {name1}')
        for t2 in ids:
            name2 = teams.loc[t2, 'name']
            team2 = format.Team(id = t2, name = name2)
            t1_win_count = 0.0

            for i in range(sim_count):
                match = format.First_To(first_to)
                match.set(blue = team1, orange = team2)
                simulate_match(match, rater, ratings)
                if match.get('winner') == team1:
                    t1_win_count += 1
            prob = t1_win_count / sim_count
            odds[name2] = prob
        list.append(odds)
    data = pd.DataFrame(list)
    data = data.set_index('winner')
    return data

def make_odds(teams, ratings):
    ids = ratings.index

    list = []
    for t1 in ids:
        odds = dict()
        name1 = teams.loc[t1, 'name']
        odds['winner'] = name1
        mu1 = ratings.loc[t1, 'mu']
        sigma1 = ratings.loc[t1, 'sigma']
        rating1 = rater.create_rating(mu = mu1, sigma = sigma1)
        for t2 in ids:
            name2 = teams.loc[t2, 'name']
            mu2 = ratings.loc[t2, 'mu']
            sigma2 = ratings.loc[t2, 'sigma']
            rating2 = rater.create_rating(mu = mu2, sigma = sigma2)
            prob = win_probability([rating1], [rating2])
            odds[name2] = prob
        list.append(odds)
    data = pd.DataFrame(list)
    data = data.set_index('winner')
    return data

def make_observed_odds(res_teams, teams, matches, games):

    wins = pd.DataFrame(0.0, index = teams.index, columns = teams.index)
    played = pd.DataFrame(0.0, index = teams.index, columns = teams.index)

    for index, game in games.iterrows():
        match_id = game['match']
        blue = matches.loc[match_id, 'blue_id']
        orange = matches.loc[match_id, 'orange_id']
        blue_won = (game['blue'] > game['orange'])
        blue_name = teams.loc[blue, 'name']
        orange_name = teams.loc[orange, 'name']
        if blue_won:
            wins.loc[blue, orange] = wins.loc[blue, orange] + 1
        else:
            wins.loc[orange, blue] = wins.loc[orange, blue] + 1
        played.loc[blue, orange] = played.loc[blue, orange] + 1
        played.loc[orange, blue] = played.loc[orange, blue] + 1

    names = []
    for id in res_teams.index:
        names.append(teams.loc[id, 'name'])

    ratio = pd.DataFrame(0, index = names, columns = names)
    for id1 in res_teams.index:
        for id2 in res_teams.index:
            win_count = wins.loc[id1, id2]
            game_count = played.loc[id1, id2]
            if game_count != 0:
                odds = win_count / game_count
            else:
                odds = None
            name1 = teams.loc[id1, 'name']
            name2 = teams.loc[id2, 'name']
            print(name1)
            print(name2)
            ratio.loc[name1, name2] = odds
    return ratio

def evaluate(teams, matches, games):

    #matches = matches.loc[matches['region'] == 'INT']
    initialize(teams)
    ratings = teams
    rater = trueskill.TrueSkill(draw_probability = 0)

    for index, row in games.iterrows():
        match_id = row['match']
        blue = matches.loc[match_id, 'blue_id']
        orange = matches.loc[match_id, 'orange_id']
        blue_won = (row['blue'] > row['orange'])

        if blue_won:
            winner = blue
            loser = orange
        else:
            winner = orange
            loser = blue
        update_with_new_ratings(ratings, rater, winner, loser)

    sorted = ratings.sort_values('mu', ascending = False)
    sorted = sorted.loc[sorted['games_played'] >= 100]
    sorted = sorted.head(7)
    return sorted

def initialize(teams):
    teams['mu'] = 25.000
    teams['sigma'] = 8.333
    teams['games_played'] = 0

def update_with_new_ratings(ratings, rater, winner, loser):
    win_pre = rater.Rating(mu = ratings.loc[winner, 'mu'], sigma = ratings.loc[winner, 'sigma'])
    loss_pre = rater.Rating(mu = ratings.loc[loser, 'mu'], sigma = ratings.loc[loser, 'sigma'])
    win_rat, loss_rat = rater.rate_1vs1(win_pre, loss_pre)
    ratings.loc[winner, 'mu'] = win_rat.mu
    ratings.loc[loser, 'mu'] = loss_rat.mu
    ratings.loc[winner, 'sigma'] = win_rat.sigma
    ratings.loc[loser, 'sigma'] = loss_rat.sigma
    ratings.loc[winner, 'games_played'] = ratings.loc[winner, 'games_played'] + 1
    ratings.loc[loser, 'games_played'] = ratings.loc[loser, 'games_played'] + 1

def win_probability(t1, t2):

    delta_mu = t1.mu - t2.mu
    sum_sigma = t1.sigma ** 2 + t2.sigma ** 2
    denom = math.sqrt(2 * (BETA * BETA) + sum_sigma)
    ts = rater
    return ts.cdf(delta_mu / denom)

def simulate_match(seeded_match, rater, ratings):
    t1 = seeded_match.get('blue').get('id')
    t2 = seeded_match.get('orange').get('id')
    m1 = ratings.loc[t1, 'mu']
    m2 = ratings.loc[t2, 'mu']
    s1 = ratings.loc[t1, 'sigma']
    s2 = ratings.loc[t2, 'sigma']
    r1 = rater.create_rating(mu = m1, sigma = s1)
    r2 = rater.create_rating(mu = m2, sigma = s2)
    while True:
        if seeded_match.get('completed'):
            break
        odds = win_probability([r1], [r2])
        sample = random()

        if odds > sample:
            winner = 'blue'
            #r1, r2 = rater.rate_1vs1(r1, r2)
        else:
            winner = 'orange'
            #r2, r1 = rater.rate_1vs1(r2, r1)

        seeded_match.set(game_winner = winner)
