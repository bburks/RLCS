data_path = '.data/rlcs2122'
output_path = 'output/rlcs2122'
from tools.data.requester import summarize_all, load
from tools.model.rater import make_odds, evaluate, make_first_to_odds, make_observed_odds
from tools.formats import format

#summarize_all(output_path)
teams = load(path = output_path, type = 'teams')
games = load(path = output_path, type = 'games')
matches = load(path = output_path, type = 'matches')
events = load(path = output_path, type = 'events')
international_events = events.loc[events['region'] == 'EU']
international_event_ids = international_events.index
international_matches = matches.loc[matches['event'].isin(international_event_ids)]
international_match_ids = international_matches.index
international_games = games.loc[games['match'].isin(international_match_ids)]


ratings = evaluate(teams, international_matches, international_games)
res = make_first_to_odds(teams, ratings, 4, 100)
res_teams = teams.loc[ratings.index]
print(res_teams)
input()
obs = make_observed_odds(res_teams, teams, international_matches, international_games)
print(ratings)
print(res)
print(obs)
#print(data)
#print(data.loc['6020bc70f1e4807cc7002386','region'])
