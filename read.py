from loss_graph import LossGraph
from eigen_rank import *
from fight import *
from utils import *

def load_fights(f):
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

    return fights

f = open('./data/fights_2018-01-06.csv', 'r')

fights = load_fights(f)

print '# of fights = ', len(fights)

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
