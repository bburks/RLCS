from . import format2 as ft

def test_best_of():
    t1 = ft.Team(id = 1, name = '1')
    t2 = ft.Team(id = 2, name = '2')
    format = ft.Best_Of(5)
    format.set_seeding([t1, t2])
    for game in format:
        game.set_winner(t2)
    assert format.get_result() == [t2, t1]
    
