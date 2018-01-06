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

class Date:
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year

class Fight:
    def __init__(self, f0, f1, result, date):
        self.f0 = f0
        self.f1 = f1
        self.result = result
        self.date = date

def is_month(s):
    months = Set(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    return s in months

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

x = Real('x')
y = Real('y')
s = Solver()
s.add(x + y > 5, x > 1, y > 1)
print(s.check())
print(s.model())
