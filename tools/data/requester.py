from octanegg import Octane
import pandas as pd
import numpy as np
import datetime
from os.path import exists

path = '.data/'

def request_events(**kwargs):
    print(kwargs)
    with Octane() as client:
        events = []
        page = 1
        while True:
            kwargs['page'] = page
            current_page_events = client.get_events(**kwargs)
            if not current_page_events:  # no more events
                break
            events += current_page_events
            page += 1


    return events

def request_matches(event_id, start = None, end = None):

    with Octane() as client:
        matches = []
        page = 1
        while True:
            current_page = client.get_matches(event = event_id, page=page, after = start, before = end)
            if not current_page:
                break
            matches += current_page
            page += 1
    return matches

def request_games(match_id, start = None, end = None):

    with Octane() as client:
        games = []
        page = 1
        while True:

            current_page = client.get_games(match = match_id, page = page, before = end, after = start)
            if not current_page:
                break
            games += current_page
            page += 1
    return games

def summarize_regions(path = '', season = 'rlcs2122', start = None, end = None):
    tags = ['id', 'name', 'start']
    regions = ['NA', 'EU', 'SAM', 'OCE', 'ME', 'ASIA', 'AF', 'INT']
    data = []
    for region in regions:
        print(f'requesting {season} events from {region}...')
        kwargs = {'group' : season, 'region' : region}
        if start != None:
            kwargs['after'] = start
        if end != None:
            kwargs['before'] = end
        events = request_events(**kwargs)
        for event in events:
            event_data = dict()
            for tag in tags:
                event_data[tag] = convert(event, 'event', tag)
            event_data['region'] = region
            data.append(event_data)
    data.sort(key = lambda x : x['start'])
    df = pd.DataFrame(data)
    _append(df, path)
    return df

def summarize_events(path = '', event_ids = [], start = None, end = None):

    tags = ['id', 'start', 'blue_score', 'orange_score', 'blue_id', 'orange_id', 'blue_name', 'orange_name']
    data = []
    for id in event_ids:
        print(f'requesting matches from event {id}...')
        matches = request_matches(id, start = start, end = end)

        for match in matches:
            match_data = dict()
            for tag in tags:
                match_data[tag] = convert(match, 'match', tag)
            match_data['event'] = id
            data.append(match_data)

    data.sort(key = lambda x : x['start'])
    df = pd.DataFrame(data)
    _append(df, path)
    return df

def summarize_matches(path = '', match_ids = [], start = None, end = None):
    data = []
    tags = ['id', 'blue', 'orange']
    count = len(match_ids)

    for i, id in enumerate(match_ids):
        print(f'requesting games from match {i+1} of {count}...')
        games = request_games(id, start = start, end = end)
        for game in games:
            info = dict()
            for tag in tags:
                info[tag] = convert(game, 'game', tag)
            info['match'] = id
            data.append(info)

    df = pd.DataFrame(data)
    _append(df, path)
    return df

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
    _append(teams, f'{path}/teams.csv')

def summarize_all(path = '', season = 'rlcs2122'):
    date_path = f'{path}/date.csv'
    date = datetime.date.today().isoformat()

    if exists(date_path):
        last_date = pd.read_csv(date_path).loc[0, '0']
    else:
        last_date = None

    if last_date == date:
        return

    #save events
    summarize_regions(path = f'{path}/events.csv', season = season)


    #save matches and gets **NEW** matches
    events = pd.read_csv(f'{path}/events.csv', keep_default_na = False)
    event_ids = events['id']
    matches = summarize_events(path = f'{path}/matches.csv',
        event_ids = event_ids, start = last_date, end = date)

    #save games from newly pulled matches
    #matches = pd.read_csv(f'{path}/matches.csv', keep_default_na = False)
    if len(matches.index) > 0:
        match_ids = matches['id']
        summarize_matches(path = f'{path}/games.csv', match_ids = match_ids)

    # save teams
    summarize_field(path = path)

    df = pd.DataFrame([[date]])
    df.to_csv(date_path)



def load(path = '', type = ''):
    full_path = f'{path}/{type}.csv'
    data = pd.read_csv(full_path, index_col = 0, keep_default_na = False)
    data = data.set_index('id')
    return data

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

def _get_event_region(events, id):
    return events.loc[events['id'] == id, 'region'].values[0]

def _append(dataframe, path):
    if exists(path):
        df = pd.read_csv(path, index_col = 0, keep_default_na = False)
        combined_df = pd.concat([df, dataframe], ignore_index = True)
        unique_df = combined_df.drop_duplicates(ignore_index = True, subset = ['id'])
        unique_df.to_csv(path)
    else:
        dataframe.to_csv(path)
