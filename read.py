from loss_graph import LossGraph
from sets import Set
from eigen_rank import *

#f = open('./data/fights_2018-01-04.csv', 'r')
f = open('./fights_2018-01-06.csv', 'r')

lines = []
for line in f.read().splitlines():
    lines.append(line)

#lines = lines[0:50000]

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
    def __init__(self, f0, f1, result, cause, date):
        self.f0 = f0
        self.f1 = f1
        self.result = result
        self.cause = cause
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
    cause = proc_line[3]

    i = 4
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

        fights.append(Fight(f1, f2, res, cause, dt))

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

# fights.sort(fight_date_cmp)
# fights = list(reversed(fights))

#print '# of fights in reversed list = ', len(fights)

X, inds, names = get_adjacency_matrix(fights)

# print("Computing the principal singular vectors using randomized_svd")
# t0 = time()
# U, s, V = randomized_svd(X, 5, n_iter=5)
# print("done in %0.3fs" % (time() - t0))

# # print the names of the wikipedia related strongest components of the
# # principal singular vector which should be similar to the highest eigenvector
# print("Top fighters according to principal singular vectors")
# pprint([names[i] for i in np.abs(U.T[0]).argsort()[-10:]])
# pprint([names[i] for i in np.abs(V[0]).argsort()[-10:]])

print("Computing principal eigenvector score using a power iteration method")
t0 = time()
scores = centrality_scores(X, max_iter=100, tol=1e-10)
print("done in %0.3fs" % (time() - t0))
pprint([names[i] for i in np.abs(scores).argsort()[-1000:]])
