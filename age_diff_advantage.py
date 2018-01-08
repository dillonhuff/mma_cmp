from eigen_rank import *
from fight import *
from utils import *
from load_fights import *
from load_fighters import *
from pprint import pprint
import matplotlib.pyplot as plt

fighters_file = open('./data/fighter_file_2018-01-06.csv', 'r')
fighters = load_fighters(fighters_file)
fighters_file.close()

print 'Loaded', len(fighters), 'fighters'

fight_file = open('./data/fights_2018-01-06.csv', 'r')
fights = load_fights(fight_file)
fight_file.close()

print 'Loaded', len(fights), 'fights'

def has_dob(fighter_name, fighters):
    if fighter_name in fighters:
        dob = fighters[fighter_name]

        return dob != 'N/A'

num_younger_wins = 0
num_fights = 0

def get_younger_fighter(fight, fighters):
    f0 = fight.f0
    f1 = fight.f1

    diff = fighters[f0].year - fighters[f1].year

    assert(diff != 0)

    # born in 1992 is younger than born in 1980, diff = 12 > 0
    if diff >= 0:
        return f0

    return f1

age_pair_wins = {}
for i in range(0, 70):
    for j in range(i + 1, 100):
        age_pair_wins[(i, j)] = {'total_fights' : 0, 'younger_wins' : 0}

abs_diff_younger_wins = {}
for i in range(0, 70):
    abs_diff_younger_wins[i] = {'total_fights' : 0, 'younger_wins' : 0}

for fight in fights:
    if ((fight.result == 'win') or (fight.result == 'loss')) and (not (fight.cause == 'DQ')):
        f0 = fight.f0
        f1 = fight.f1

        if has_dob(f0, fighters) and has_dob(f1, fighters):
            # 1995 - 1985 = 10, positive means f0 is YOUNGER!
            diff = fighters[f0].year - fighters[f1].year

            # If the fighters are not the same age
            if diff != 0:
                abs_diff = abs(diff)
                num_fights += 1
                winner = get_winner(fight)
                younger = get_younger_fighter(fight, fighters)

                older = f1 if younger == f0 else f0

                abs_diff_younger_wins[abs_diff]['total_fights'] = abs_diff_younger_wins[abs_diff]['total_fights'] + 1

                fight_year = fight.date.year
                younger_age = fight_year - fighters[younger].year
                older_age = fight_year - fighters[older].year

                if not (younger_age > 0) or not (older_age > 0):
                    print 'Skipping malformed record'
                    print 'Fighter = ', younger
                    print 'Date of birth =', fighters[younger].to_string()
                    print 'Opponent =', older
                    print 'Date of birth =', fighters[older].to_string()
                    print 'Date of fight =', fight.date.to_string()
                    print 'younger_age = ', younger_age
                    continue

                assert(younger_age > 0)

                assert(older_age > 0)

                age_pair_wins[(younger_age, older_age)]['total_fights'] = age_pair_wins[(younger_age, older_age)]['total_fights'] + 1
                
                if winner == younger:
                    num_younger_wins += 1
                    abs_diff_younger_wins[abs_diff]['younger_wins'] = abs_diff_younger_wins[abs_diff]['younger_wins'] + 1
                    age_pair_wins[(younger_age, older_age)]['younger_wins'] = age_pair_wins[(younger_age, older_age)]['younger_wins'] + 1
                    

print 'Abs diff wins'
pprint(abs_diff_younger_wins)

deleted = True
while deleted:
    deleted = False
    for key in age_pair_wins:
        if age_pair_wins[key]['total_fights'] < 1:
            del age_pair_wins[key]
            deleted = True
            break

print 'Age pair wins'
pprint(age_pair_wins)

print '# of fights =', num_fights
print '# of fights won by younger fighter =', num_younger_wins
print '% of fights won by younger fighter =', (num_younger_wins / float(num_fights))*100.0

age_diffs = []
win_pcts = []
print 'Younger win ratios by age'
for i in xrange(1, 25):
    if abs_diff_younger_wins[i]['total_fights'] != 0:
        young_win_pct = (abs_diff_younger_wins[i]['younger_wins'] / float(abs_diff_younger_wins[i]['total_fights'])) * 100.0
        win_pcts.append(young_win_pct)
        age_diffs.append(i)

        print 'Diff = ', i, ', Younger win percentage =', young_win_pct
    else:
        print 'Diff = ', i, 'Younger win percentage UNDEFINED'
    

plt.scatter(age_diffs, win_pcts)
plt.plot(age_diffs, win_pcts)
plt.show()
