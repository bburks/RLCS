
from tools.data.extract_data import pull_rlcs_data
import tools.formats.format
from tools.model.rater import Rater
from tools.model.data_connector import get_all_connected_rlcs_matches
from tools.model.model import get_region_strengths
import os
#pull_rlcs_data(path = '.data')


def iterate_ratings():
    matches = get_all_connected_rlcs_matches(regions = ['INT'])
    last_dict = dict()
    for _ in range(1):
        print(_)
        model = Rater(ratings = last_dict)
        model.evaluate(matches)
        last_dict = model.ratings


    teams = []
    for team in model.ratings:
        teams.append(team)

    teams.sort(key = lambda team : [model.ratings[team].mu])

    for team in teams:
        print(f"{team.get('name')} - {model.ratings[team].mu} +- {model.ratings[team].sigma}")

get_region_strengths('output/winter_major')
