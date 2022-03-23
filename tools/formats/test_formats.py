from . import format, swiss, bracket, RLCS as rlcs
from ..data import data_handler

def make_teams(count):
    return [format.Team(i) for i in range(count)]

def complete(event):

    capacity = event.get('capacity')
    seeding = make_teams(capacity)
    event.set(seeding = seeding)
    i = 0
    while not event.get('completed') and i < 100:
        i += 1
        ready_matches = event.get('ready_matches')
        for match in ready_matches:
            goal = match.get('win_goal')
            match.set(score = (0, goal))
    assert event.get('completed')
    return event

def complete_5050(event):
    capacity = event.get('capacity')
    seeding = make_teams(capacity)
    event.set(seeding = seeding)
    i = 0
    j = 0
    while not event.get('completed') and i < 100:
        i += 1
        ready_matches = event.get('ready_matches')
        for match in ready_matches:
            goal = match.get('win_goal')
            j += 1
            if j % 2 == 1:
                match.set(score = (0, goal))
            else:
                match.set(score = (goal, 0))
    assert event.get('completed')
    return event


def test_swiss_sixteen_save():
    teams = [format.Team(i) for i in range(16)]
    event = swiss.Swiss_Sixteen()
    path = 'test_data/swiss_saving'
    data_handler.mkdir(path)
    event.set(seeding = teams)
    ready_matches = event.get('ready_matches')

    for match in ready_matches:
        match.set(score = (3,2))
    event.get('ready_matches')
    event.save(f'{path}/0')
    same_event = swiss.Swiss_Sixteen.load(f'{path}/0')
    assert event == same_event

def test_swiss_sixteen_completion():

    event = swiss.Swiss_Sixteen()
    complete(event)
    assert event.get('result') == event.get('seeding')

def test_trivial():
    event = complete(format.Trivial())
    assert event.get('result') == event.get('seeding')

def test_join():
    event = format.Join(format.Trivial(), format.Trivial())
    event = complete(event)
    assert event.get('result') == event.get('seeding')

def test_parallel():
    event = format.Parallel(format.Trivial(), format.Trivial())
    event = complete(event)
    assert event.get('result') == event.get('seeding')

def test_single_elim():
    event = complete(format.Single_Elim(2))

    assert event.get('result') == event.get('seeding')

def test_double_final():
    event = complete(format.Double_Final())
    assert event.get('result') == event.get('seeding')
    event = complete_5050(format.Double_Final())
    assert event.get('result') == event.get('seeding')

def test_RLCS_Fall():
    event = rlcs.Fall_2122_Regional()
    complete(event)
    assert event.get('result') == event.get('seeding')
