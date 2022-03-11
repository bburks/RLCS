
import sys

def collapse(list):
    new = []
    for elem in list:
        if new.count(elem) == 0:
            new.append(elem)
    return new

def transpose(dataList):
    return list(map(list, zip(*dataList)))







if __name__ == '__main__':

    teams = []
    for i in range(6):
        teams.append(format.Team(i))
    banned = [[1, 2], [3, 4], [1, 5], [0, 5]]
    banned_matchups = []
    for pair in banned:
        banned_matchup = format.Match()
        banned_matchup.set('orange', teams[pair[0]])
        banned_matchup.set('blue', teams[pair[1]])
        banned_matchups.append(banned_matchup)
    res = generate_matchups(teams, banned_matchups)
    print(res)
