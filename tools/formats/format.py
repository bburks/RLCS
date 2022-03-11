import math
from ..data import csv_handler

class Format:

    def __init__(self):

        self.seeding = None

    def get(self, str, **kwargs):
        if str == 'completed':
            matches = self.get('matches')
            for match in matches:
                match_completed = match.get('completed')
                if not match_completed:
                    return False
            return True

        if str == 'ready':
            if self.seeding == None:
                return False
            if self.get('completed'):
                return False
            return True
        if str == 'ready_matches':
            ready_matches = []
            for match in self.get('matches'):
                if match.get('ready'):
                    ready_matches.append(match)
            return ready_matches
        if str == 'seeding':
            return self.seeding

        # Must be implemented in subclass
        if str == 'matches':
            pass
        # Must be implemented in subclass
        if str == 'result':
            pass

    def set(self, **kwargs):
        for str in kwargs:
            obj = kwargs[str]
            if str == 'seeding':
                self.seeding = obj

    def save(self, path):
        matches = []
        labels = ['orange', 'blue', 'score']
        dataList = [[], [], []]
        for match in self.get('matches'):
            info = []
            for i, label in emuerate(labels):
                info[i].append(match.get(label))
        csv_handler.export(labels, dataList, path)



class Match:
    def __init__(self):
        self.orange_team = None
        self.blue_team = None
        self.score = None

    def get(self, str):
        if str == 'orange':
            return self.orange_team
        if str == 'blue':

            return self.blue_team

        if str == 'winner':
            if self.score[0] - self.score[1] > 0:
                return self.blue_team
            else:
                return self.orange_team
        if str == 'loser':
            if self.score[0] - self.score[1] < 0:
                return self.blue_team
            else:
                return self.orange_team
        if str == 'score':
            return self.score

        if str == 'seeded':
            if self.orange_team == None or self.blue_team == None:
                return False
            return True
        if str == 'completed':
            if self.score == None:
                return False
            return True

        if str == 'ready':
            if self.get('completed'):
                return False
            if self.get('seeded'):
                return True
            return False

    def set(self, **kwargs):
        for str in kwargs:
            obj = kwargs[str]
            if str == 'orange':
                assert  isinstance(obj, Team), 'assigned team must be a team object'
                self.orange_team = obj
            elif str == 'blue':
                assert isinstance(obj, Team), 'assigned team must be a team object'
                self.blue_team = obj
            elif str == 'score':

                assert  isinstance(obj, tuple), 'score must be a tuple'
                assert obj[0] != obj[1], 'match cannot end in a tie'
                self.score = obj

    def __repr__(self):
        if self.get('ready'):
            return f"{self.get('blue')} vs {self.get('orange')}"
        if self.get('completed'):
            return f"{self.get('blue')} vs {self.get('orange')} | {self.get('score')}"
        else:
            return 'unseeded match'

class Team:

    def __init__(self, id):
        self.id = id

    def get(self, str):
        if str == 'id':
            return self.id

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, Team):
            if self.id == other.id:
                return True
        return False

    def __repr__(self):
        return f'T{self.id}'



class Single_Elim_Bracket(Format):

    def __init__(self, team_count, win_goals):
        round_count = math.log(team_count, 2)
        assert round_count == int(round_count), 'team_count must be a power of 2'
        round_count = int(round_count)
        rounds = []
        round_match_count = team_count
        for i, win_goal in zip(range(round_count), win_goals):
            round_match_count = round_match_count // 2


            rounds.append(Outside_In(round_match_count, win_goal))
        self.rounds = rounds

    def get(self, str, **kwargs):

        if str == 'matches':
            matches = []
            for round in self.get('rounds'):
                matches.extend(round.get('matches'))
            return matches
        if str == 'result':
            res = dict()
            for i, round in enumerate(self.get('rounds')):
                for match in round.get('matches'):
                    if not match.get('completed'):
                        continue
                    loser = match.get('loser')

        if str == 'seeding':
            team = kwargs['team']
            return self.seeding[team]
        if str == 'opponent':
            round = self.get('rounds')[kwargs['round']]
            team = kwargs['team']

            for match in self.get('round_matches'):
                if team == match.get('blue'):
                    return match.get('orange')
                if team == match.get('orange'):
                    return match.get('blue')
        if str == 'rounds':
            return self.rounds
        if str == 'round_match_count':
            round = kwargs['round']
            return len(self.get('round_matches', round = round))
        if str == 'round_matches':
            round = self.get('rounds')[kwargs['round']]
            return round.get('matches')
        if str == 'round_seed':
            round = kwargs['round']
            seeding = kwargs['seeding']
            max_seed = 2 ** len(self.get('rounds')) - 1
            current_seed = seeding

            for i in range(round):
                max_seed = (max_seed - 1) // 2
                if current_seed <= max_seed:
                    current_seed = 2 * max_seed + 1 - current_seed
                current_seed -= max_seed + 1
            return current_seed

        return super().get(self, str, **kwargs)

    def set(self, **kwargs):
        for str in kwargs:
            obj = kwargs[str]
            if str == 'seeding':
                self.seeding = obj

class Fall_2122_Regional(Format):
    def __init__():
        self.swiss = Sixteen_Swiss()
        self.playoff = Single_Elim_Bracket(8, [4, 4, 4])

    def get(self, str, **kwargs):
        if str == 'matches':
            matches = []
            matches.extend(self.swiss.get('matches'))
            matches.extend(self.playoff.get('matches'))
            return matches

        if str == 'result':
            return self.playoff.get('result')

    def set(self, **kwargs):
        pass



class First_To(Match):

    def __init__(self, win_goal):
        super().__init__()
        self.win_goal = win_goal

    def get(self, str):
        if str == 'win_goal':
            return self.win_goal
        return super().get(str)

    def set(self, **kwargs):
        for str in kwargs:
            obj = kwargs[str]
            if str == 'score':
                assert  max(obj[0], obj[1]) == self.win_goal, f'completed match winner must win {self.win_goal} games'
                super().set(score = obj)
            else:
                super().set(**kwargs)
