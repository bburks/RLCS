class Time:

    def __init__(self, str):
        spot = 0
        times = ['', '', '', '', '', '']
        dividers = ['-','-','T',':',':','Z']
        labels = ['year', 'month', 'day', 'hour', 'minute', 'second']
        time = ''
        for char in str:
            if char == dividers[spot]:
                times[spot] = time
                spot += 1
                time = ''
            else:
                time = f'{time}{char}'

        self.times = times
        self.labels = labels




t = Time('2020-07-29T18:00:00Z')
print(t.times)
