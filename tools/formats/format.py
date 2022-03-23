import math
from ..data import csv_handler, data_handler

class Format:
    # subclasses should implement:
    # _update_match_seeding(self)
    # _update_result(self)
    # self.matches or self.get('matches')
    # self.capacity or self.get('capacity')

    def __init__(self):
        self.matches = None
        self.seeding = None
        self.result = None
        self.capacity = None

    def get(self, str, **kwargs):
        if str == 'completed':
            matches = self.get('matches')
            for match in matches:
                match_completed = match.get('completed')
                if not match_completed:
                    return False
            return True
        elif str == 'ready_matches':
            self._update_match_seeding()
            ready_matches = []
            for match in self.get('matches'):
                if match.get('ready'):
                    ready_matches.append(match)
            return ready_matches
        elif str == 'seeding':
            return self.seeding
        elif str == 'matches':
            return self.matches
        elif str == 'result':
            if self.get('completed') and self.result == None:
                self._update_result()
            return self.result
        elif str == 'seed':
            team = kwargs['team']
            for i, t in enumerate(self.get('seeding')):
                if t == team:
                    return i
            return None
        elif str == 'capacity':
            return self.capacity
        else:
            assert False, f'{str} not recognized'

    def set(self, **kwargs):
        for str in kwargs:
            obj = kwargs[str]
            if str == 'seeding':
                assert isinstance(obj, list)
                self.seeding = obj
            else:
                assert False, f'{str} not recognized'

    def save(self, path):
        data_handler.mkdir(path)
        matches = []
        labels = ['blue', 'orange', 'blue_score', 'orange_score']
        dataList = [[], [], [], []]
        for match in self.get('matches'):
            for i, label in enumerate(labels):
                dataList[i].append(match.get(label))
        csv_handler.export(labels, dataList, f'{path}/matches')
        seeding = self.get('seeding')
        csv_handler.export_line(seeding, f'{path}/seeding')

    @classmethod
    def load(cls, path):
        [labels, dataList] = csv_handler.extract(f'{path}/matches')
        seeding = csv_handler.extract_line(f'{path}/seeding')
        seeding = [int(seed) for seed in seeding]
        funcs = [Team, Team, lambda x : x, lambda x : x]
        loaded = cls()

        for func, label, data in zip(funcs, labels, dataList):
            for match, datum in zip(loaded.get('matches'), data):
                if datum == '':
                    continue
                else:
                    datum = func(int(datum))

                kwargs = dict()
                kwargs[label] = datum

                match.set(**kwargs)
        loaded.set(seeding = seeding)
        return loaded


    def _update_match_seeding(self):
        assert False, 'this function should be overridden'

    def _update_result(self):
        assert False, 'this function should be overridden'


    def __repr__(self):
        return self.get('matches').__repr__()

    def __eq__(self, other):
        if not isinstance(other, Format):
            return False
        for m1, m2 in zip(self.get('matches'), other.get('matches')):
            if m1 != m2:
                return False
        return True

class Match:
    def __init__(self):
        self.orange_team = None
        self.blue_team = None
        self.blue_score = None
        self.orange_score = None
        self.date = None

    def get(self, str):

        if str == 'blue':
            return self.blue_team
        elif str == 'orange':
            return self.orange_team
        elif str == 'blue_score':
            return self.blue_score
        elif str == 'orange_score':
            return self.orange_score

        elif str == 'winner':
            if not self.get('completed'):
                return None
            if self.get('blue_score') > self.get('orange_score'):
                return self.get('blue')
            else:
                return self.get('orange')
        elif str == 'loser':
            if not self.get('completed'):
                return None
            if self.get('blue_score') > self.get('orange_score'):
                return self.get('orange')
            else:
                return self.get('blue')

        elif str == 'score':
            return (self.get('blue_score'), self.get('orange_score'))

        elif str == 'seeded':
            if self.orange_team == None or self.blue_team == None:
                return False
            return True
        elif str == 'completed':
            if self.orange_score == None or self.blue_score == None:
                return False
            return True
        elif str == 'ready':
            if self.get('completed'):
                return False
            if self.get('seeded'):
                return True
            return False

        elif str == 'date':
            return self.date

        else:
            assert False, f'{str} not recognized'

    def set(self, **kwargs):
        for str in kwargs:
            obj = kwargs[str]
            if str == 'blue':
                assert isinstance(obj, Team), 'assigned team must be a team object'
                self.blue_team = obj
            elif str == 'orange':
                assert  isinstance(obj, Team), 'assigned team must be a team object'
                self.orange_team = obj
            elif str == 'score':

                assert  isinstance(obj, tuple), 'score must be a tuple'
                assert obj[0] != obj[1], 'match cannot en in a tie'
                self.set(blue_score = obj[0])
                self.set(orange_score = obj[1])
            elif str == 'blue_score':

                self.blue_score = int(obj)
            elif str == 'orange_score':

                self.orange_score = int(obj)
            elif str == 'date':
                self.date = obj
            else:
                assert False, f'{str} not recognized'

    def __repr__(self):
        if self.get('ready'):
            return f"{self.get('blue')} vs {self.get('orange')}"
        if self.get('completed'):
            return f"{self.get('blue')} vs {self.get('orange')} | {self.get('score')}"
        else:
            return f"None vs None"

    def __eq__(self, other):
        if not isinstance(other, Match):
            return False
        for label in ['orange', 'blue', 'orange_score', 'blue_score']:
            if self.get(label) != other.get(label):
                return False
        return True

class Team:

    def __init__(self, id):
        self.id = id
        self.name = None

    def get(self, str):
        if str == 'id':
            return self.id
        if str == 'name':
            return self.name
        if str == 'region':
            return self.region

    def set(self, **kwargs):
        for key in kwargs:
            obj = kwargs[key]
            if key == "name":
                self.name = obj
            if key == 'region':
                self.region = obj

    def __hash__(self):
        return self.id.__hash__()

    def __eq__(self, other):
        if isinstance(other, Team):
            if self.id == other.id:
                return True
        return False

    def __repr__(self):
        return f'{self.id}'

class First_To(Match):
    def __init__(self, win_goal = 3):
        super().__init__()
        self.win_goal = win_goal

    def set(self, **kwargs):
        for str in kwargs:
            obj = kwargs[str]
            if str == 'orange_score':
                assert obj <= self.win_goal
                blue_score = self.get('blue_score')
                if blue_score != None:
                    assert max(blue_score, obj) == self.win_goal
            elif str == 'blue_score':
                assert obj <= self.win_goal
                orange_score = self.get('orange_score')
                if orange_score != None:
                    assert max(orange_score, obj) == self.win_goal


        super().set(**kwargs)

    def get(self, str):
        if str == 'win_goal':
            return self.win_goal
        else:
            return super().get(str)

class Join(Format):
    def __init__(self, F1, F2):
        super().__init__()
        self.F1 = F1
        self.F2 = F2



    def get(self, str, **kwargs):

        if str == 'seeding':
            return self.F1.get('seeding')
        elif str == 'matches':
            matches = []
            for event in [self.F1, self.F2]:
                matches.extend(event.get('matches'))
            return matches
        elif str == 'capacity':
            return self.F1.get('capacity')
        else:
            return super().get(str, **kwargs)

    def set(self, **kwargs):
        for str in kwargs:
            obj = kwargs[str]
            if str == 'seeding':
                self.F1.set(seeding = obj)
            else:
                super().set(**kwargs)

    def _update_match_seeding(self):
        self.F1._update_match_seeding()
        if self.F1.get('completed'):
            self.F1._update_result()
            res = self.F1.get('result')
            self.F2.set(seeding = res[0:self.F2.get('capacity')])
            self.F2._update_match_seeding()

    def _update_result(self):

        if not self.get('completed'):
            return None
        res = []
        high = self.F2.get('result')
        low = self.F1.get('result')[self.F2.get('capacity'):]
        res.extend(high)
        res.extend(low)
        self.result = res




    def __repr__(self):
        return f'{self.F1.__repr__()} | {self.F2.__repr__()}'

class Parallel(Format):
    def __init__(self, F1, F2):
        super().__init__()
        self.upper = F1
        self.lower = F2
        self.matches = []
        self.capacity = F1.get('capacity') + F2.get('capacity')
        for event in [self.upper, self.lower]:
            self.matches.extend(event.get('matches'))

    def set(self, **kwargs):
        for str in kwargs:
            obj = kwargs[str]
            if str == 'seeding':
                seeding = obj
                us = []
                ls = []
                for i, seed in enumerate(seeding):
                    mod = i % 4
                    if mod == 0 or mod == 3:
                        us.append(seed)
                    else:
                        ls.append(seed)
                self.upper.set(seeding = us)
                self.lower.set(seeding = ls)
                self.seeding = seeding
            else:
                super().set(**kwargs)

    def _update_match_seeding(self):
        for event in [self.upper, self.lower]:
            event._update_match_seeding()

    def _update_result(self):
        ur = self.upper.get('result')
        lr = self.lower.get('result')
        res = []
        for u, l in zip(ur, lr):
            teams = [u, l]

            teams.sort(key = lambda x : self.get('seed', team = x))
            res.extend(teams)
        self.result = res

class Trivial(Format):
    def __init__(self, win_goal = 3):
        super().__init__()
        self.matches = [First_To(win_goal = win_goal)]
        self.capacity = 2

    def _update_match_seeding(self):
        seeding = self.get('seeding')
        if seeding == None:
            return None
        match = self.get('matches')[0]
        match.set(orange = seeding[0], blue = seeding[1])

    def _update_result(self):
        if not self.get('completed'):
            return
        winner = self.get('matches')[0].get('winner')
        loser = self.get('matches')[0].get('loser')
        self.result = [winner, loser]

class Single_Elim(Join):
    def __init__(self, round_count = 3, win_goals = [4, 4, 4]):
        assert isinstance(round_count, int)
        assert round_count >= 2
        assert round_count <= 10
        if round_count == 2:
            upper = Trivial(win_goal = win_goals[0])
            lower = Trivial(win_goal = win_goals[0])
        else:
            upper = Single_Elim(round_count - 1, win_goals = win_goals[:-1])
            lower = Single_Elim(round_count - 1, win_goals = win_goals[:-1])
        first = Parallel(upper, lower)
        last = Trivial(win_goal = win_goals[-1])
        super().__init__(first, last)

class Double_Final(Format):
    def __init__(self, win_goal = 4):
        super().__init__()
        self.matches = [First_To(win_goal = win_goal) for _ in range(3)]
        self.capacity = 2


    def _update_match_seeding(self):
        seeding = self.get('seeding')
        if seeding == None:
            return None
        matches = self.get('matches')
        for i, match in enumerate(matches):
            if i == 0 or i == 1:
                match.set(blue = seeding[1], orange = seeding[0])
            if i == 2:
                first = matches[0]
                second = matches[1]
                if first.get('completed') and second.get('completed'):
                    if first.get('winner') != second.get('winner'):
                        match.set(blue = seeding[1], orange = seeding[0])
                    else:
                        self.matches.pop()

    def _update_result(self):
        if self.get('completed'):
            last = self.get('matches')[-1]
            self.result = [last.get('winner'), last.get('loser')]
