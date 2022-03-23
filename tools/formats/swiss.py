from . import format
import math


class Swiss_Sixteen(format.Format):

    def __init__(self):
        super().__init__()
        matches = []
        for _ in range(27):
            matches.append(format.First_To(3))
        self.matches = matches
        self.round_starts = [0, 8, 12, 16, 18, 22, 24, 27, 30, 33]
        self.capacity = 16

    def _update_match_seeding(self):
        for i in range(3):
            for j in range(3):

                self._seed_round(i, j)

    def _update_result(self):
        if not self.get('completed'):
            return None
        scores = dict()
        seeding = self.get('seeding')
        for initial_seed, team in enumerate(seeding):
            scores[team] = [0, 0, - initial_seed]
            win_count, loss_count = 0, 0
        for match in self.get('matches'):
            match_score = match.get('score')
            diff = abs(match_score[0] - match_score[1])
            winner = match.get('winner')
            loser = match.get('loser')
            scores[winner][0] = scores[winner][0] + 1
            scores[winner][1] = scores[winner][1] + diff
            scores[loser][0] = scores[loser][0] - 1
            scores[loser][1] = scores[loser][1] - diff
        teams = []
        teams.extend(seeding)
        teams.sort(key = lambda x : scores[x], reverse = True)
        self.result = teams

    def _get_matches(self, win_count, loss_count):
        lookup = [[0, 12, 22], [8, 18, 27], [16, 24, 30]]
        length = [[8, 4, 2], [4, 4, 3], [2, 3, 3]]
        start = lookup[win_count][loss_count]
        end = start + length[win_count][loss_count]
        return self.matches[start : end]

    def _seed_round(self, win_count, loss_count):


        recent_matches = []
        round_teams = []
        if win_count > 0:
            matches = self._get_matches(win_count - 1, loss_count)
            recent_matches.extend(matches)
            for match in matches:
                round_teams.append(match.get('winner'))

        if loss_count > 0:
            matches = self._get_matches(win_count, loss_count - 1)
            recent_matches.extend(matches)
            for match in matches:
                round_teams.append(match.get('loser'))

        prior_matches = []
        for i in range(win_count + 1):
            for j in range(loss_count + 1):
                if i == win_count and j == loss_count:
                    continue
                prior_matches.extend(self._get_matches(i, j))

        for match in prior_matches:
            if not match.get('completed'):
                return None


        seeding_scores = dict()
        for team in round_teams:
            for i, t in enumerate(self.get('seeding')):
                if team == t:
                    initial_seed = i

            w = 0
            l = 0
            while True:

                if w == win_count and l == loss_count:
                    break
                if w == win_count and l == loss_count - 1:
                    from_upper = True
                if w == win_count - 1 and l == loss_count:
                    from_upper = False
                game_diff = 0
                matches = self._get_matches(w, l)
                for match in matches:
                    if match.get('winner') == team:
                        score = match.get('score')
                        game_diff += abs(score[0] - score[1])
                        w += 1
                    if match.get('loser') == team:
                        score = match.get('score')
                        game_diff -= abs(score[0] - score[1])
                        l+= 1
            seeding_scores[team] = [from_upper, game_diff, - initial_seed]
        round_teams.sort(key = lambda x : seeding_scores[x], reverse = True)

        matches = self._get_matches(win_count, loss_count)
        if win_count == 0 and loss_count == 0:
            matches_template = Swiss_Sixteen._setup_matches(self.get('seeding'), prior_matches)
        else:
            matches_template = Swiss_Sixteen._setup_matches(round_teams, prior_matches)
        for match, match_template in zip(matches, matches_template):
            match.set(blue = match_template.get('blue'))
            match.set(orange = match_template.get('orange'))

    @staticmethod
    def _setup_matches(seeding, banned_matches):
        if seeding == []:
            return []
        top_seed = seeding[0]
        team_count = len(seeding)
        for i in range(team_count):
            preferred_opponent = seeding[team_count - i - 1]
            if Swiss_Sixteen._is_included(top_seed, preferred_opponent, banned_matches):
                continue
            other_teams = []
            other_teams.extend(seeding[1 : team_count - i - 1])
            other_teams.extend(seeding[team_count - i :])
            other_matches = Swiss_Sixteen._setup_matches(other_teams, banned_matches)
            if other_matches == None:
                continue

            match = format.Match()
            match.set(orange = top_seed, blue = preferred_opponent)
            other_matches.append(match)
            return other_matches
        return None

    @staticmethod
    def _is_included(t1, t2, matches):
        for match in matches:
            if t1 == match.get('blue') and t2 == match.get('orange'):
                return True
            if t2 == match.get('blue') and t1 == match.get('orange'):
                return True
        return False

    def _get_seeding_score(self, team, round_count):
        win_count = 0
        loss_count = 0
        diff = 0
        from_upper = False
        for i in range(round_count):
            round = self.get(
            'round', win_count = win_count, loss_count = loss_count)
            if not round.get('completed'):
                return None
            res = round.get('result')[team]
            diff += res
            if res > 0:
                win_count += 1
            else:
                loss_count += 1
            if i == round_count - 1:
                if res < 0:
                    from_upper = True

            # diff will be total game differential. still need to get initial seed and from_upper

        for i, t in enumerate(self.get('teams')):
            if t == team:
                initial_seed = i
        return [from_upper, diff, - initial_seed]
