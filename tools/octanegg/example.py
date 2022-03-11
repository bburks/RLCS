from collections import Counter
from octanegg import Octane
from itertools import chain

with Octane() as client:
    games = []
    page = 1
    while True:
        current_page_games = client.get_games(tier='S', after='2021-01-01',
                                              before='2021-06-20', page=page)
        if not current_page_games:  # no more games
            break
        games += current_page_games
        page += 1

num_games = len(games)
blue_players = ([player.get('player').get('tag') for player in game.get('blue').get('players')] for game in games)
orange_players = ([player.get('player').get('tag') for player in game.get('orange').get('players')] for game in games)
players = list(chain.from_iterable(blue_players)) + list(chain.from_iterable(orange_players))
player_counts = Counter(players)

print(f'In our time window, there were {num_games} NA S-tier games.')
print(f'The 6 most seen players were: ')
print(player_counts.most_common(6))
