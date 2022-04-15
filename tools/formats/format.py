from abc import ABC, abstractmethod
from random import random
class Format(ABC):

    def __init__(self):
        self.seeding = None

    def set_seeding(self, seeding):
        assert isinstance(seeding, list)
        assert len(seeding) == self.get_capacity()

        self.seeding = seeding

    def is_seeded(self):
        if self.seeding == None:
            return False
        return True

    def get_seeding(self):
        return self.seeding

    def __iter__(self):
        return self

    def fill(self, mode = 0):
        teams = [Team(id = i + 1, name = str(i + 1)) for i in range(self.get_capacity())]
        self.set_seeding(teams)
        for game in self:
            if mode == 0:
                game.set_winner(game.get_blue())
            elif mode == 1:
                game.set_winner(game.get_orange())
            elif mode == 2:
                if random() < 0.5:
                    game.set_winner(game.get_blue())
                else:
                    game.set_winner(game.get_orange())
            else:
                assert False

    




    @abstractmethod
    def is_completed(self):
        pass

    @abstractmethod
    def get_capacity(self):
        pass

    @abstractmethod
    def get_result(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

class Game:
    def __init__(self):
        self.blue = None
        self.orange = None
        self.winner = None

    def get_blue(self):
        return self.blue

    def get_orange(self):
        return self.orange

    def get_winner(self):
        return self.winner

    def is_completed(self):
        if self.winner == None:
            return False
        else:
            return True

    def is_seeded(self):
        if self.get_blue() == None:
            return False
        if self.get_orange() == None:
            return False
        return True

    def is_ready(self):
        if self.is_completed():
            return False
        if self.is_seeded():
            return True
        return False

    def set_blue(self, team):
        self.blue = team

    def set_orange(self, team):
        self.orange = team

    def set_winner(self, team):
        assert team == self.get_orange() or team == self.get_blue()
        self.winner = team

    def __repr__(self):
        return f'{self.get_blue()} vs {self.get_orange()} | winner: {self.get_winner()}'

class Team:
    def __init__(self, id = None, name = None, region = None):
        self.id = id
        self.name = name
        self.region = region

    def get_name(self):
        return self.name
    def get_id(self):
        return self.id
    def get_region(self):
        return self.region

    def set_id(self, id):
        self.id = id
    def set_name(self, name):
        self.name = name
    def set_region(self, region):
        self.region = region

    def __hash__(self):
        return self.get_id().__hash__()
    def __eq__(self, other):
        if isinstance(other, Team):
            if self.get_id() == other.get_id():
                return True
        return False
    def __repr__(self):
        return f'{self.get_name()}'



class Best_Of(Format):
    def __init__(self, max_game_count):
        super().__init__()
        assert isinstance(max_game_count, int)
        assert max_game_count > 0
        assert max_game_count < 100
        assert max_game_count % 2 == 1
        self.win_goal = (max_game_count + 1) / 2
        self.games = []

    def _get_status(self):
        if not self.is_seeded():
            return 0
        blue_count = 0
        orange_count = 0
        for game in self.games:
            if not game.is_completed():
                return 1
            if game.get_winner() == game.get_blue():
                blue_count += 1
            else:
                orange_count += 1
        if blue_count == self.win_goal:
            seeding = self.get_seeding()
            return [seeding[0], seeding[1]]
        elif orange_count == self.win_goal:
            seeding = self.get_seeding()
            return [seeding[1], seeding[0]]
        else:
            return 1

    def is_completed(self):
        status = self._get_status()
        if status == 0 or status == 1:
            return False
        return True

    def get_capacity(self):
        return 2

    def get_result(self):
        status = self._get_status()
        if status == 0 or status == 1:
            return None
        return status

    def __next__(self):
        if self.is_completed():
            raise StopIteration
        for game in self.games:
            if not game.is_completed():
                return game
        game = Game()
        seeding = self.get_seeding()
        game.set_blue(seeding[0])
        game.set_orange(seeding[1])
        self.games.append(game)
        return game

    def __repr__(self):
        if self.is_completed():
            res = self.get_result()
            return f'{res[0]} / {res[1]}'
        if self.is_seeded():
            seeding = self.get_seeding()
            return f'{seeding[0]} vs {seeding[1]}'
        return 'unseeded match'

class Bracket_Reset(Format):
    def __init__(self, match_length):
        super().__init__()
        self.match_length = match_length
        self.matches = []

    def is_completed(self):
        n = len(self.matches)
        if n == 0:
            return False
        match = self.matches[-1]
        if not match.is_completed():
            return False
        if n == 1:
            if match.get_result() == self.get_seeding():
                return True
            return False
        if n == 2:
            return True

    def get_capacity(self):
        return 2

    def get_result(self):
        if self.is_completed():
            return self.matches[-1].get_result()
        return None

    def __next__(self):
        n = len(self.matches)
        if n == 0:
            match = Best_Of(self.match_length)
            match.set_seeding(self.get_seeding())
            self.matches.append(match)
            return match.__next__()
        if n == 1:
            if not self.matches[0].is_completed():
                return self.matches[0].__next__()
            match = Best_Of(self.match_length)
            match.set_seeding(self.get_seeding())
            self.matches.append(match)
            return match.__next__()
        if n == 2:
            if not self.matches[1].is_completed():
                return self.matches[1].__next__()
            raise StopIteration


    def __repr__(self):
        if self.is_completed():
            res = self.get_result()
            return f'{res[0]} / {res[1]}'
        return f'Bracket_Reset'



class Parallel(Format):
    def __init__(self, f1, f2):
        super().__init__()
        self.f1 = f1
        self.f2 = f2

    def set_seeding(self, teams):
        super().set_seeding(teams)
        s1 = []
        s2 = []
        for i, team in enumerate(teams):
            if i % 4 == 0 or i % 4 == 3:
                s1.append(team)
            else:
                s2.append(team)
        self.f1.set_seeding(s1)
        self.f2.set_seeding(s2)

    def is_completed(self):
        return self.f2.is_completed() and self.f1.is_completed()

    def get_capacity(self):
        return self.f1.get_capacity() + self.f2.get_capacity()

    def get_result(self):
        r1 = self.f1.get_result()
        r2 = self.f2.get_result()
        if r1 == None or r2 == None:
            return None
        i1 = 0
        i2 = 0
        res = []
        for i in range(self.get_capacity()):
            if i % 4 == 0 or i % 4 == 3:
                res.append(r1[i1])
                i1 += 1
            else:
                res.append(r2[i2])
                i2 += 1
        return res

    def __next__(self):
        if self.f2.is_completed():
            raise StopIteration
        if self.f1.is_completed():
            return self.f2.__next__()
        return self.f1.__next__()

    def __repr__(self):
        return f'[{self.f1} | {self.f2}]'

class Join(Format):

    def __init__(self, f1, f2):
        super().__init__()
        self.f1 = f1
        self.f2 = f2

    def set_seeding(self, seeding):
        super().set_seeding(seeding)
        self.f1.set_seeding(seeding)

    def is_completed(self):
        return self.f2.is_completed()

    def get_capacity(self):
        return self.f1.get_capacity()

    def get_result(self):
        if not self.f2.is_completed():
            return None
        eliminated = self.f1.get_result()[self.f2.get_capacity():]
        res = self.f2.get_result()
        res.extend(eliminated)
        return res

    def __next__(self):
        if not self.f1.is_completed():
            return self.f1.__next__()
        if not self.f2.is_seeded():
            print(f'seeding next event: {self.f2}')
            res = self.f1.get_result()
            self.f2.set_seeding(res[0:self.f2.get_capacity()])
        if self.f2.is_completed():
            raise StopIteration
        return self.f2.__next__()

    def __repr__(self):
        return f'{self.f1} -> {self.f2}'

class Permute(Format):

    def __init__(self, ft, permutation):
        super().__init__()
        self.permutation = permutation
        self.ft = ft
        assert ft.get_capacity() == len(permutation)

    def set_seeding(self, teams):
        super().set_seeding(teams)
        self.ft.set_seeding(teams)

    def is_completed(self):
        return self.ft.is_completed()

    def get_capacity(self):
        return len(self.permutation)

    def get_result(self):
        res = self.ft.get_result()
        if res == None:
            return None
        permuted = [0] * len(self.permutation)
        for team, i in zip(res, self.permutation):
            permuted[i - 1] = team
        return permuted

    def __next__(self):
        return self.ft.__next__()

    def __repr__(self):
        return f'{self.ft}'

class Over_Seed(Format):
        def __init__(self, ft, extra_team_count):
            super().__init__()
            self.extra_team_count = extra_team_count
            self.ft = ft

        def set_seeding(self, teams):
            super().set_seeding(teams)
            self.ft.set_seeding(teams[self.extra_team_count:])

        def is_completed(self):
            return self.ft.is_completed()

        def get_capacity(self):
            return self.ft.get_capacity() + self.extra_team_count

        def get_result(self):
            lower = self.ft.get_result()
            if lower == None:
                return None
            upper = self.get_seeding()[0:self.extra_team_count]
            upper.extend(lower)
            return upper

        def __next__(self):
            return self.ft.__next__()

        def __repr__(self):
            return f'{self.ft}'
            return f'{self.get_seeding()[0:self.extra_team_count]} + {self.ft}'



class Single_Elim(Join):
    def __init__(self, round_count, match_lengths):
        assert len(match_lengths) == round_count

        if round_count == 2:
            first = match_lengths[0]
            start = Parallel(Best_Of(first), Best_Of(first))
            last = match_lengths[1]
            end = Best_Of(last)
            super().__init__(start, end)
        else:
            s1 = Single_Elim(round_count - 1, match_lengths[0:round_count - 1])
            s2 = Single_Elim(round_count - 1, match_lengths[0:round_count - 1])
            start = Parallel(s1, s2)
            end = Best_Of(match_lengths[-1])
            super().__init__(start, end)

class Lower_Bracket(Join):
    def __init__(self, upper_round_count, match_lengths):
        assert upper_round_count * 2 - 2 == len(match_lengths)
        if upper_round_count == 2:
            first = Over_Seed(Best_Of(match_lengths[0]), 1)
            second = Best_Of(match_lengths[1])
            super().__init__(first, second)
        else:
            l1 = Lower_Bracket(upper_round_count - 1, match_lengths[:2 * upper_round_count - 4])
            l2 = Lower_Bracket(upper_round_count - 1, match_lengths[:2 * upper_round_count - 4])
            first = Over_Seed(Parallel(l1, l2), 1)
            second = Lower_Bracket(2, [match_lengths[-2], match_lengths[-1]])
            super().__init__(first, second)

class Spring2122(Join):
    def __init__(self):
        upper = Single_Elim(4, [5, 5, 7, 7])
        lower = Over_Seed(Lower_Bracket(4, [5, 5, 5, 7, 7, 7]), 1)
        final = Bracket_Reset(7)
        #permutation = [i + 1 for i in range(16)]
        permutation = [1, 2, 3, 4, 7, 8, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16]
        upper_to_lower = Permute(upper, permutation)
        start = Join(upper_to_lower, lower)
        super().__init__(start, final)
