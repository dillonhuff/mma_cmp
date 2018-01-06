from loss_graph import LossGraph

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

lg = LossGraph()

for line in proc_lines:
    fighter0 = line[0]
    fighter1 = line[1]

    result = line[2]

    if result == 'loss':
        lg.addFight(fighter1, fighter0)
    elif result == 'win':
        lg.addFight(fighter0, fighter1)

print 'Jon Jones beat ', lg.fighter_wins("/fighter/Jon-Jones-27944")
print 'Jon Jones lost to ', lg.fighter_losses("/fighter/Jon-Jones-27944")

# for fighter in lg.getFighters():

#     if len(lg.fighter_losses(fighter)) == 0:
#         print fighter, 'is undefeated with', len(lg.fighter_wins(fighter)), 'wins'

x = Real('x')
y = Real('y')
s = Solver()
s.add(x + y > 5, x > 1, y > 1)
print(s.check())
print(s.model())
