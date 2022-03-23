from . import data_connector, model
from ..formats import swiss, format
event_path = '.data/rlcs2122/NA/1'
def make_teams(count):
    return [format.Team(i) for i in range(count)]

def complete(event):
    if event.get('seeding') == None:
        capacity = event.get('capacity')
        seeding = make_teams(capacity)
        event.set(seeding = seeding)
    i = 0
    while not event.get('completed') and i < 100:
        i += 1

        ready_matches = event.get('ready_matches')
        for match in ready_matches:
            win_goal = match.get('win_goal')
            match.set(score = (win_goal - 1, win_goal))
    assert event.get('completed')
    return event

def test_connector():

    assert data_connector.get_event_date(event_path) == '2021-10-24T23:00:00Z'

def test_match_paths():
    assert len(data_connector.get_match_paths(event_path)) == 75

def test_event_stages():
    res = data_connector.get_event_stages(event_path)

def test_trueskill():

    my_bracket = format.Single_Elim(3)
    complete(my_bracket)
    my_model = model.TrueSkill(my_bracket.get('matches'))
    for i in range(8):
        print(my_model.ratings[format.Team(i)])

def test_trueskill_simulation():

    teams = make_teams(16)
    e1, e2 = format.Single_Elim(round_count = 3), format.Single_Elim(round_count = 3)
    e1.set(seeding = teams)
    complete(e1)
    e2.set(seeding = e1.get('result'))

    M = model.TrueSkill(e1.get('matches'))
    res = M.simulate(e2)
    print(res)





"""
def test_simulate():
    event = format.Single_Elim()
    teams = make_teams(8)
    event.set(seeding = teams)
    my_model = model.TrueSkill()
    res = my_model.simulate(event)
    print(f'simulation result : {res}')
"""
