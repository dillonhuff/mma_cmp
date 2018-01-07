from fight import *
from utils import *

f = open('./data/fighter_file_2018-01-06.csv', 'r')

fighters = {}
for line in f.read().splitlines():
    toks = line.split('\t')

    assert(len(toks) == 3)

    name = toks[0]
    dob = toks[2]

    if (dob == 'N/A'):
        fighters[name] = dob
    else:
        dob_toks = dob.split('-')
        assert(len(dob_toks) == 3)

        year = dob_toks[0]
        month = dob_toks[1]
        day = dob_toks[2]

        assert(represents_int(year))
        assert(represents_int(day))
        assert(represents_int(month))

        fighters[name] = Date(num_to_month(int(month)), int(day), int(year))


print '# of fighters = ', len(fighters)
jl_dob = fighters['/fighter/Jared-Luna-78075']

print '/fighter/Jared-Luna-78075 DOB =', jl_dob.to_string()
