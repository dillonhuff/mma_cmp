class Date:
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year

    def month_num(self):
        return month_to_num(self.month)

    def to_string(self):
        return self.month + '-' + str(self.day) + '-' + str(self.year)

class Fighter:
    def __init__(self, name, date_of_birth):
        self.name = name
        self.date_of_birth = date_of_birth

class Fight:
    def __init__(self, f0, f1, result, cause, date):
        self.f0 = f0
        self.f1 = f1
        self.result = result
        self.cause = cause
        self.date = date

def date_cmp(a, b):
    if a.year > b.year:
        return -1

    if a.year < b.year:
        return 1

    # same year

    if a.month_num() > b.month_num():
        return -1

    if a.month_num() < b.month_num():
        return 1

    # same month
    if a.day > b.day:
        return -1

    return 1
    
def fight_date_cmp(a, b):
    ad = a.date
    bd = b.date
    return date_cmp(ad, bd)

def get_winner(fight):
    assert((fight.result == 'win') or (fight.result == 'loss'))

    if fight.result == 'win':
        return fight.f0

    return fight.f1
