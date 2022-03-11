import csv_handler as csv
from helper import collapse


class Season:
    def __init__(self, path):
        self.path = path
        event_count = list_count(path)
        events = []

        for i in range(event_count):
            event = Event(f'{path}/{i}')
            events.append(event)
        self.events = events.sort(key = lambda x : x.start)

class Event:
    def __init__(self, path):
        #self.teams = teams
        self.start = csv.extract_one(f'{path}/startDate')
        #self.end = end

        matches = []
        duplicated_teams = []

        match_count = list_count(f'{path}/matches')
        for i in range(match_count):
            match = Match(f'{path}/matches/{i}')
            matches.append(match)
            duplicated_teams.append(match.blue)
            duplicated_teams.append(match.orange)

        self.teams = collapse(duplicated_teams)
        self.matches = matches

class Match:
    def __init__(self, path):

        self.path = path

        blue_id = csv.extract_one(f'{path}/blue/team/team/_id')
        orange_id = csv.extract_one(f'{path}/orange/team/team/_id')
        blue_name = csv.extract_one(f'{path}/blue/team/team/name')
        orange_name = csv.extract_one(f'{path}/orange/team/team/name')
        blue_win_count = self.get_score('blue')
        orange_win_count = self.get_score('orange')


        self.blue = Team(blue_id, blue_name)
        self.orange = Team(orange_id, orange_name)
        self.score = (blue_win_count, orange_win_count)

    def get_score(self, color):

        try:
            score = int(csv.extract_one(f'{self.path}/{color}/score'))
        except:
            score = 0
        return score

class Game:
    def __init__(self, orange, blue, score):
        self.orange = orange
        self.blue = blue
        self.score = score

class Team:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

class Player:
    def __init__(self, id, tag):
        self.id = id
        self.tag = tag

class Time:

    def __init__(self, str):
        spot = 0
        times = ['', '', '', '', '', '']
        dividers = ['-','-','T',':',':','Z']
        labels = ['year', 'month', 'day', 'hour', 'minute', 'second']
        for char in str:
            if char == dividers[spot]:
                spot += 1
            else:
                times[spot] = f'{times[spot]}{char}'
        self.times = times
        self.labels = labels

    def __eq__(self, other):
        return self.times == other.times

def list_count(path):
    return int(csv.extract_one(f'{path}/count'))
