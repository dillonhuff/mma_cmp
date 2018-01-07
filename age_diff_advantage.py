from eigen_rank import *
from fight import *
from utils import *
from load_fights import *
from load_fighters import *

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

for fight in fights:
    if ((fight.result == 'win') or (fight.result == 'loss')) and (not (fight.cause == 'DQ')):
        f0 = fight.f0
        f1 = fight.f1

        if has_dob(f0, fighters) and has_dob(f1, fighters):
            print f0, 'born', fighters[f0].to_string()
            print f1, 'born', fighters[f1].to_string()
            print 'Age diff = ', fighters[f1].year - fighters[f0].year, 'years'
            
                
