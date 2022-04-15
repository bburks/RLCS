from . import format, swiss, bracket

class Fall_2122_Regional(format.Join):
    def __init__(self):
        myswiss = swiss.Swiss_Sixteen()
        playoff1 = format.Single_Elim(2)
        playoff2 = format.Single_Elim(2)
        final = format.Double_Final()
        playoff_start = format.Parallel(playoff1, playoff2)
        playoff = format.Join(playoff_start, final)
        super().__init__(myswiss, playoff)

class Spring_2122_Regional(format.Join):
    upper = bracket.Single_Elim(team_count = 16, win_goals = [3, 3, 4, 4])
