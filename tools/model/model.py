from .data_connector import get_all_connected_rlcs_matches
from .rater import Rater
from ..data.data_handler import log_summary
from ..helper import contains, mkdir


def get_region_strengths(path):
    mkdir(path)
    region_weights = dict()
    region_totals = dict()
    region_averages = dict()
    region_counts = dict()
    matches = get_all_connected_rlcs_matches(regions = ['INT'])
    rater = Rater()
    rater.evaluate(matches)

    team_infos = []
    print(len(rater.ratings))
    for team in rater.ratings:



        r = rater.ratings[team]
        name = team.get('name')
        id = team.get('id')
        region = team.get('region')
        info = dict()
        info['id'] = id
        info['name'] = name
        info['mu'] = r.mu
        info['sigma'] = r.sigma
        info['region'] = region
        team_infos.append(info)

        if not contains(region_weights, region):
            region_weights[region] = 0
            region_totals[region] = 0
            region_counts[region]`` = 0
        region_weights[region] = region_weights[region] + (1 / r.sigma)
        region_totals[region] = region_totals[region] + (r.mu / r.sigma)
        region_counts[region] = region_counts[region] + 1

    region_infos = []
    for region in region_weights:
        region_average = region_totals[region] / region_weights[region]
        region_info = dict()
        region_info['region'] = region
        region_info['average_rating'] = region_average
        region_info['team_count'] = region_counts[region]
        region_infos.append(region_info)

    log_summary(region_infos, f'{path}/region_summary')

    log_summary(team_infos, f'{path}/team_summary')
