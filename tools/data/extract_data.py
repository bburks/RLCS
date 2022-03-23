from octanegg import Octane
from . import csv_handler as csv
from .data_handler import log
from ..helper import mkdir


path = '.data/'

FALL_MAJOR_ID = '614b6589f8090ec745286426'

def request_events(**kwargs):
    with Octane() as client:

        events = []
        page = 1
        while True:
            current_page_events = client.get_events(page=page, **kwargs)
            if not current_page_events:  # no more events
                break
            events += current_page_events
            page += 1

    return events

def request_matches(event_id):
    with Octane() as client:
        matches = []
        page = 1
        while True:
            current_page = client.get_matches(event = event_id, page=page)
            if not current_page:
                break
            matches += current_page
            page += 1
    return matches

def request_games(match_id):
    with Octane() as client:
        games = []
        page = 1
        while True:
            current_page = client.get_games(match = match_id, page=page)
            if not current_page:
                break
            games += current_page
            page += 1
    return games

def log_events(regions = [], path = '', group = ''):

    mkdir(f'{path}/{group}/')

    for region in regions:
        events = request_events(group = group, region = region)
        log(events, f'{path}/{group}/{region}')

def log_matches(path):
    count = int(csv.extract_one(f'{path}/count'))
    for i in range(count):
        event_path = f'{path}/{i}'
        event_id = csv.extract_one(f'{event_path}/_id')
        matches = request_matches(event_id)
        log(matches, f'{event_path}/matches')

def log_games(path):
    event_count = int(csv.extract_one(f'{path}/count'))
    for i in range(match_count):
        event_path = f'{path}/{i}'
        matches_path = f'{event_path}/{matches}'
        match_count = int(csv.extract_one(f'{path}/count'))
        for j in range(match_count):
            match_path = f'{matches_path}/{i}'
            games = request_games(match_id)
            log(games, f'{match_path}/games')

def pull_rlcs_data(path = '', season = 'rlcs2122'):
    group = season
    regions = ['NA', 'EU', 'SAM', 'OCE', 'ME', 'ASIA', 'AF', 'INT']
    #log_events(regions = regions, path = path, group = group)
    for region in regions:
        region_path = f'{path}/{season}/{region}'
        event_count = int(csv.extract_one(f'{region_path}/count'))
        for i in range(event_count):
            event_path = f'{region_path}/{i}'
            event_id = csv.extract_one(f'{event_path}/_id')
            event_matches = request_matches(event_id)
            log(event_matches, f'{event_path}/matches')



#log_events(regions = ['NA', 'EU'], path = 'data', group = 'rlcsx')
#log_matches('data/rlcsx/EU')
#log_matches('data/rlcsx/NA')
#log_games('data/rlcsx/EU')
#log_games('data/rlcsx/NA')





#extract_events(tier = 'S', path = f'{path}S/')
#extract_events(tier = 'A')

#matches = request_matches('614b6589f8090ec745286426')
#print(matches)
#games = request_games('61a752b5f8090ec74528e3dd')
#request_and_export_all(path)
