from octanegg import Octane
from . import csv_handler as csv
from .logger import log
from ..helper import mkdir
import pandas as pd
import numpy as np

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

def log_rlcs_data(path = '', season = 'rlcs2122'):
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

def convert(item, f, to):
    try:
        if f == 'event':
            if to == 'id':
                return item['_id']
            elif to == 'name':
                return item['name']
            elif to == 'start':
                return item['startDate']
            elif to == 'region':
                return item['region']
            else:
                print('unrecognized key')
        elif f == 'match':
            if to == 'id':
                return item['_id']
            elif to == 'start':
                return item['date']
            elif to == 'blue_score':
                return item['blue']['score']
            elif to == 'orange_score':
                return item['orange']['score']
            elif to == 'blue_id':
                return item['blue']['team']['team']['_id']
            elif to == 'orange_id':
                return item['orange']['team']['team']['_id']
            elif to == 'blue_name':
                return item['blue']['team']['team']['name']
            elif to == 'orange_name':
                return item['orange']['team']['team']['name']
            else:
                print('unrecognized key')
        elif f == 'game':
            if to == 'id':
                return item['_id']
            elif to == 'blue':
                return item['blue']['team']['stats']['core']['goals']
            elif to == 'orange':
                return item['orange']['team']['stats']['core']['goals']
            else:
                print('unrecognized key')
        else:
            print('unrecognized key')
    except KeyError:

        return np.NaN
    except:
        print('something went wrong')

def summarize_regions(path = '', season = 'rlcs2122'):
    tags = ['id', 'name', 'start']
    group = season
    regions = ['NA', 'EU', 'SAM', 'OCE', 'ME', 'ASIA', 'AF', 'INT']
    data = []
    for region in regions:
        print(f'requesting {season} events from {region}...')
        events = request_events(group = group, region = region)
        for event in events:
            event_data = dict()
            for tag in tags:
                event_data[tag] = convert(event, 'event', tag)
            event_data['region'] = region
            data.append(event_data)
    data.sort(key = lambda x : x['start'])
    dataFrame = pd.DataFrame(data)
    dataFrame.to_csv(path)

def summarize_events(path = '', event_ids = []):

    tags = ['id', 'start', 'blue_score', 'orange_score', 'blue_id', 'orange_id', 'blue_name', 'orange_name']
    data = []
    for id in event_ids:
        print(f'requesting matches from event {id}...')
        matches = request_matches(id)

        for match in matches:
            match_data = dict()
            for tag in tags:
                match_data[tag] = convert(match, 'match', tag)
            match_data['event'] = id
            data.append(match_data)

    data.sort(key = lambda x : x['start'])
    dataFrame = pd.DataFrame(data)
    dataFrame.to_csv(path)

def summarize_matches(path = '', match_ids = []):
    data = []
    tags = ['id', 'blue', 'orange']
    count = len(match_ids)

    for i, id in enumerate(match_ids):
        print(f'requesting games from match {i+1} of {count}...')
        games = request_games(id)
        for game in games:
            info = dict()
            for tag in tags:
                info[tag] = convert(game, 'game', tag)
            info['match'] = id
            data.append(info)
            print(info)

    dataFrame = pd.DataFrame(data)
    dataFrame.to_csv(path)

def summarize_all(path = '', season = 'rlcs2122'):

    #save events
    summarize_season(path = f'{path}/events.csv')

    #save matches
    events = pd.read_csv(f'{path}/events.csv', keep_default_na = False)
    event_ids = events['id']
    summarize_events(path = f'{path}/matches.csv', event_ids = event_ids)

    #save games
    matches = pd.read_csv(f'{path}/matches.csv', keep_default_na = False)
    match_ids = matches['id']
    summarize_matches(path = f'{path}/games.csv', match_ids = match_ids)

    # save teams
    summarize_field(path = f'{path}/teams.csv')

def summarize_field(path = '', season = 'rlcs2122'):
    events = pd.read_csv(f'{path}/events.csv', keep_default_na = False)
    matches = pd.read_csv(f'{path}/matches.csv', keep_default_na = False)
    event_regions = events.loc[:, ['id', 'region']]

    teams = matches.loc[:, ['blue_id', 'orange_id', 'blue_name', 'orange_name']]
    blues = matches.loc[:, ['blue_id', 'blue_name', 'event']]
    blues = blues.rename(columns = {'blue_id' : 'id', 'blue_name' : 'name'})
    oranges = matches.loc[:, ['orange_id', 'orange_name', 'event']]
    oranges = oranges.rename(columns = {'orange_id' : 'id', 'orange_name' : 'name'})
    teams = pd.concat([oranges, blues]).drop_duplicates(subset = ['id'])

    teams['region'] = teams['event'].apply(lambda x : _get_event_region(events, x))
    teams = teams.loc[: , ['id', 'name', 'region']]
    teams = teams.sort_values(['region', 'name'])
    teams = teams.reset_index()
    del teams['index']
    teams.to_csv(path)
    #print(teams.to_string())
    #print(_get_event_region(events, '614b7046f8090ec74528642d'))
    #print(teams.loc[teams['name'] == 'GracesBlaze Refine'])
    #print(matches)
    #print(teams)
    #print(blues)

    #unique_blues = blues.drop_duplicates()
    #print(blues)
    #print(unique_blues)
    #print(event_regions)

def load(path = '', type = ''):
    full_path = f'{path}/{type}.csv'
    data = pd.read_csv(full_path, index_col = 0, keep_default_na = False)
    data = data.sort_values('id')
    data = data.set_index('id')
    return data

def _get_event_region(events, id):
    return events.loc[events['id'] == id, 'region'].values[0]
