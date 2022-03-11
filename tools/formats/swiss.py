import format


class Swiss_Round(format.Format):

    def __init__(self, match_count, win_goal):
        self.win_goal = win_goal
        self.matches = []
        for i in range(match_count):
            match = First_To(self.win_goal)
            self.matches.append(match)

    def get(self, str, **kwargs):
        if str == 'matches':
            return self.matches
        if str == 'winners':
            winners = []
            for match in self:
                winners.append(match.get('winner'))
            return winners
        if str == 'losers':
            losers = []
            for match in self:
                losers.append(match.get('loser'))
            return losers
        if str == 'teams':
            teams = []
            for match in self.matches:
                teams.append(match.get('blue'))
                teams.append(match.get('orange'))
        if str == 'result':
            res = dict()
            for match in self.get('matches'):
                winner = match.get('winner')
                loser = match.get('loser')
                score = match.get('score')
                res[winner] = abs(score[1] - score[0])
                res[loser] = - abs(score[1] - score[0])
            return res

    def set(self, **kwargs):
        for str in kwargs:
            obj = kwargs[str]
            if str == 'seeding':
                banned_matches = kwargs['banned_matches']
                self.matches = _generate_matches(seeding, banned_matches)




    def __repr__(self):
        return self.get('matches')

class Swiss_Sixteen(format.Format):

    def __init__(self):

        rounds = []
        for win_count in range(3):
            for loss_count in range(3):
                match_count = int(
                8 * math.factorial(win_count + loss_count) /
                (math.factorial(win_count) * math.factorial(loss_count) *
                2 ** (win_count + loss_count)))
                round = Swiss_Round(match_count, 5)
                rounds.append(round)
        self.rounds = rounds

    def get(self, str, **kwargs):

        if str == 'matches':
            matches = []
            for round in self.get('rounds'):
                matches.extend(round.get('matches'))
            return matches

        if str == 'rounds':
            return self.rounds

        if str == 'round':
            win_count = kwargs['win_count']
            loss_count = kwargs['loss_count']
            return self.rounds[3 * win_count + loss_count]

        if str == 'teams':
            return list(self.seeding.keys())

        if str == 'ready_matches':
            self._update()
            return super().get(str, **kwargs)

        return super().get(str, **kwargs)

    def set(self, **kwargs):
        for str in kwargs:
            obj = kwargs[str]
            if str == 'seeding':
                self.seeding = obj

    def _update(self):
        pass

    def _seed_round(self, win_count, loss_count):

    def



def _generate_matches(seeding, banned_matches):
    top_seed = seeding[0]
    team_count = len(seeding)
    for i in len(teams - 1):
        preferred_opponent = seeding[-i - 1]
        if _included(top_seed, preferred_opponent, banned_matches):
            continue

        other_teams = []
        other_teams.extend(seeding[1:-i-1])
        other_teams.extend(seeding[-i:])
        other_matches = _generate_matches(other_teams, banned_matches)
        if other_matches == None:
            continue
        match = format.First_To(self.win_goal)

        return [match] + [other_matches]




    return None

def _included(t1, t2, banned_matches):
    for match in banned_matches:
        if t1 == match.get('orange') and t2 = match.get('blue'):
            return True
        if t2 == match.get('orange') and t1 = match.get('blue'):
            return True
    return False
