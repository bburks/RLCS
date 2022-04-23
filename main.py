data_path = '.data/rlcs2122'
output_path = 'output/rlcs2122'
from tools.data.requester import summarize_all, load
from tools.model.model import Model, get_game, evaluate_region
from tools.formats import format

REGIONS = ['NA', 'EU', 'SAM', 'ASIA', 'AF', 'ME', 'OCE']

summarize_all(output_path)

teams = load(path = output_path, type = 'teams')
games = load(path = output_path, type = 'games')
matches = load(path = output_path, type = 'matches')
events = load(path = output_path, type = 'events')
"""
model = Model()
for index, row in games.iterrows():
    game = get_game(matches, row)
    model.update_ratings(game)
model.save(output_path)
"""
for region in REGIONS:
    evaluate_region(region, output_path)
evaluate_region('INT', output_path)
