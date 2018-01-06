from loss_graph import LossGraph
from sets import Set
from z3 import *

f = open('./fights_2018-01-04.csv', 'r')



lines = []
for line in f.read().splitlines():
    lines.append(line)
    
print '# of lines = ', len(lines)

proc_lines = []

for line in lines:
    tokens = []

    for tok in line.split(' '):
        for tk in tok.split('\t'):
            tokens.append(tk)

    proc_lines.append(tokens)

def is_month(s):
    months = Set(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    return s in months

def month_to_num(s):
    month_nums = {'Jan' : 0,
                  'Feb' : 1,
                  'Mar' : 2,
                  'Apr' : 3,
                  'May' : 4,
                  'Jun' : 5,
                  'Jul' : 6,
                  'Aug' : 7,
                  'Sep' : 8,
                  'Oct' : 9,
                  'Nov' : 10,
                  'Dec' : 11}

    return month_nums[s]
    
class Date:
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year

    def month_num(self):
        return month_to_num(self.month)

    def to_string(self):
        return self.month + '-' + str(self.day) + '-' + str(self.year)

class Fight:
    def __init__(self, f0, f1, result, date):
        self.f0 = f0
        self.f1 = f1
        self.result = result
        self.date = date

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

fights = []
for proc_line in proc_lines:
    f1 = proc_line[0]
    f2 = proc_line[1]
    res = proc_line[2]

    i = 3
    while not is_month(proc_line[i]):
        i += 1

    assert(is_month(proc_line[i]))

    month = proc_line[i]

    assert(proc_line[i + 1] == '/')

    day = proc_line[i + 2]

    assert(proc_line[i + 3] == '/')

    year = proc_line[i + 4]

    if represents_int(year) and represents_int(day):
        dt = Date(month, int(day), int(year))

        fights.append(Fight(f1, f2, res, dt))

print '# of fights = ', len(fights)

print 'Sorting fights by date'

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

fights.sort(fight_date_cmp)
fights = reversed(fights)

# for fight in fights:
#     print fight.f0, fight.f1, fight.result, ', ', fight.date.month, '/', fight.date.day, '/', fight.date.year

# lg = LossGraph()

# for line in proc_lines:
#     fighter0 = line[0]
#     fighter1 = line[1]

#     result = line[2]

#     if result == 'loss':
#         lg.addFight(fighter1, fighter0)
#     elif result == 'win':
#         lg.addFight(fighter0, fighter1)

# print 'Jon Jones beat ', lg.fighter_wins("/fighter/Jon-Jones-27944")
# print 'Jon Jones lost to ', lg.fighter_losses("/fighter/Jon-Jones-27944")

# for fighter in lg.getFighters():

#     if len(lg.fighter_losses(fighter)) == 0:
#         print fighter, 'is undefeated with', len(lg.fighter_wins(fighter)), 'wins'

print 'Setting up optimization problem'
s = Solver()

for fight in fights:
    if (fight.result == 'win') or (fight.result == 'loss'):
        f0_dt = fight.f0 + '-' + fight.date.to_string()
        f1_dt = fight.f1 + '-' + fight.date.to_string()

        f0v = Real(f0_dt)
        f1v = Real(f1_dt)

        if (fight.result == 'win'):
            s.add(f0v > f1v)
        else:
            s.add(f1v > f0v)

print 'Checking model...'
print(s.check())

print(s.model())
