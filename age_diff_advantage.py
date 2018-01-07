from eigen_rank import *
from fight import *
from utils import *
from load_fights import *
from load_fighters import *
from pprint import pprint

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

age_diff_records = {}
for i in range(-100, 100):
    age_diff_records[i] = {'win' : 0, 'loss' : 0}

for fight in fights:
    if ((fight.result == 'win') or (fight.result == 'loss')) and (not (fight.cause == 'DQ')):
        f0 = fight.f0
        f1 = fight.f1

        if has_dob(f0, fighters) and has_dob(f1, fighters):
            num_fights += 1
            # 1995 - 1985 = 10, positive means f0 is YOUNGER!
            diff = fighters[f0].year - fighters[f1].year

            # If the fighters are not the same age
            if diff != 0:
                winner = get_winner(fight)
                younger = get_younger_fighter(fight, fighters)
                if winner == younger:
                    num_younger_wins += 1
            
            if fight.result == 'win':
                age_diff_records[diff]['win'] = age_diff_records[diff]['win'] + 1
            else:
                age_diff_records[diff]['loss'] = age_diff_records[diff]['loss'] + 1

pprint(age_diff_records)                

print '# of fights =', num_fights
print '# of fights won by younger fighter =', num_younger_wins
print '% of fights won by younger fighter =', (num_younger_wins / float(num_fights))*100.0
