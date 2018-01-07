from loss_graph import LossGraph
from eigen_rank import *
from fight import *
from utils import *
from load_fights import *

f = open('./data/fights_2018-01-06.csv', 'r')

fights = load_fights(f)

print '# of fights = ', len(fights)

X, inds, names = get_adjacency_matrix(fights)

print("Computing principal eigenvector score using a power iteration method")

t0 = time()
scores = centrality_scores(X, max_iter=100, tol=1e-10)

print("done in %0.3fs" % (time() - t0))

pprint([names[i] for i in np.abs(scores).argsort()[-1000:]])
