from ..formats import format
import trueskill

class Rater:
    def __init__(self, ratings = dict()):
        self.ratings = ratings
        self.model = trueskill.TrueSkill(draw_probability = 0)

    def _rated(self, team):
        for t in self.ratings:
            if t == team:
                return True
        return False

    def _add(self, team):
        self.ratings[team] = self.model.create_rating()

    def _safe_add(self, team):
        if self._rated(team):
            return None
        self._add(team)

    def evaluate(self, completed_matches):
        for match in completed_matches:
            teams = [match.get('winner'), match.get('loser')]
            self._safe_add(teams[0])
            self._safe_add(teams[1])
            wr, lr = self.model.rate_1vs1(self.ratings[teams[0]], self.ratings[teams[1]])
            self.ratings[teams[0]] = wr
            self.ratings[teams[1]] = lr
