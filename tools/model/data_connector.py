from ..data import csv_handler as csv
from ..formats import format

def get_event_paths(region_path):
    count = int(csv.extract_one(f'{region_path}/count'))
    event_paths = []
    for i in range(count):
        event_paths.append(f'{region_path}/{i}')
    event_paths.sort(key = get_event_date)
    return event_paths

def get_event_date(event_path):
    return csv.extract_one(f'{event_path}/startDate')

def get_match_paths(event_path):
    count = int(csv.extract_one(f'{event_path}/matches/count'))
    paths = []
    for i in range(count):
        paths.append(f'{event_path}/matches/{i}')
    paths.sort(key = get_match_date)

    return paths

def get_event_stages(event_path):
    count = int(csv.extract_one(f'{event_path}/stages/count'))
    res = dict()
    for i in range(count):
        id = int(csv.extract_one(f'{event_path}/stages/{i}/_id'))
        name = csv.extract_one(f'{event_path}/stages/{i}/name')
        res[id] = name

    resdic = []
    for i in range(count):
        resdic.append(res[i])
    return resdic

def get_team_ids(match_path):
    blue_path = f'{match_path}/blue/team/team'
    orange_path = f'{match_path}/orange/team/team'
    blue_id = csv.extract_one(f'{blue_path}/_id')
    orange_id = csv.extract_one(f'{orange_path}/_id')
    return (blue_id, orange_id)

def get_team_names(match_path):
    blue_path = f'{match_path}/blue/team/team'
    orange_path = f'{match_path}/orange/team/team'
    blue_name = csv.extract_one(f'{blue_path}/name')
    orange_name = csv.extract_one(f'{orange_path}/name')
    return (blue_name, orange_name)

def get_team_regions(event_region, match_path):
    if event_region != 'INT':
        return (event_region, event_region)

    blue_path = f'{match_path}/blue/team/team'
    orange_path = f'{match_path}/orange/team/team'
    blue = csv.extract_one(f'{blue_path}/region')
    orange = csv.extract_one(f'{orange_path}/region')
    return (blue, orange)

def get_match_score(match_path):
    blue_path = f'{match_path}/blue'
    orange_path = f'{match_path}/orange'
    try:
        blue_score = int(csv.extract_one(f'{blue_path}/score'))
    except:
        blue_score = 0
    try:
        orange_score = int(csv.extract_one(f'{orange_path}/score'))
    except:
        orange_score = 0
    return (blue_score, orange_score)

def get_match_stage(match_path):
    return int(csv.extract_one(f'{match_path}/stage/_id'))

def get_match_date(match_path):
    return csv.extract_one(f'{match_path}/date')

def make_match(event_region, match_path):

    score = get_match_score(match_path)
    if score == (0, 0):
        return None
    match = format.First_To(max(score[0], score[1]))
    team_ids = get_team_ids(match_path)
    team_names = get_team_names(match_path)
    team_regions = get_team_regions(event_region, match_path)
    teams = [format.Team(team_ids[0]), format.Team(team_ids[1])]
    teams[0].set(name = team_names[0])
    teams[1].set(name = team_names[1])
    teams[0].set(region = team_regions[0])
    teams[1].set(region = team_regions[1])
    date = get_match_date(match_path)

    match.set(score = score, blue = teams[0], orange = teams[1], date = date)
    return match

def get_all_connected_rlcs_matches(regions = ['NA', 'EU', 'ME', 'SAM', 'OCE', 'ASIA', 'INT']):

    base_path = '.data/rlcs2122'
    matches = []
    for region in regions:
        region_path = f'{base_path}/{region}'
        event_paths = get_event_paths(region_path)
        for event_path in event_paths:
            match_paths = get_match_paths(event_path)
            for match_path in match_paths:
                match = make_match(region, match_path)
                if match == None:
                    continue
                matches.append(match)
    matches.sort(key = lambda x : x.get('date'))
    return matches
