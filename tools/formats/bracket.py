from . import format, swiss
import math

class Single_Elim(format.Format):

    def __init__(self, team_count = 8, win_goals = [3, 3, 3]):
        round_count = math.log(team_count, 2)
        assert round_count == int(round_count), 'team_count must be a power of 2'
        round_count = int(round_count)
        rounds = []
        round_match_count = team_count
        for i, win_goal in zip(range(round_count), win_goals):
            round_match_count = round_match_count // 2
            rounds.append(swiss.Swiss_Round(round_match_count, win_goal))
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

            return self.seeding
        if str == 'rounds':
            return self.rounds
        if str == 'ready_matches':
            self._update()
            return super().get('ready_matches')

        return super().get(str, **kwargs)

    def set(self, **kwargs):
        for str in kwargs:
            obj = kwargs[str]
            if False:
                pass
            else:
                kwarg = dict()
                kwarg[str] = obj
                super().set(**kwarg)

    def _get_round_seed(self, round, team):

        seeding = self.get('seeding')
        for i, other_team in enumerate(seeding):
            if team == other_team:
                seed = i
                break


        max_seed = 2 ** len(self.get('rounds')) - 1
        current_seed = seed
        for i in range(round):
            max_seed = (max_seed - 1) // 2
            if current_seed > max_seed:
                current_seed = max_seed - current_seed
        return current_seed

    def _seed_round(self, round_count):
        initial_seeding = self.get('seeding')
        seeding_scores = dict()
        unsorted_teams = []
        round = self.get('rounds')[round_count]
        if round.get('completed'):
            return None
        if round_count == 0:
            round.set(seeding = initial_seeding, banned_matches = [])
        else:
            prior_round = self.get('rounds')[round_count - 1]
            if prior_round.get('completed'):
                for match in prior_round.get('matches'):
                    winner = match.get('winner')
                    unsorted_teams.append(winner)
                    seeding_scores[winner] = self._get_round_seed(round_count, winner)
                unsorted_teams.sort(key = lambda x : seeding_scores[x])

                round.set(seeding = unsorted_teams, banned_matches = [])

    def _update(self):
        round_count = len(self.get('rounds'))
        for i in range(round_count):
            self._seed_round(i)

class RLCS_2122_Playoff(format.Format):
    def __init__(self, team_count = 8, win_goals = [3, 3, 3]):
        self.bracket = Single_Elim(team_count = 8, win_goals = [3, 3, 3])
        self.final = Double_Final()
