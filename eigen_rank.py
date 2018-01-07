# Author: Olivier Grisel <olivier.grisel@ensta.org>
# License: BSD 3 clause

from __future__ import print_function

from bz2 import BZ2File
import os
from datetime import datetime
from pprint import pprint
from time import time

import numpy as np

from scipy import sparse

from sklearn.decomposition import randomized_svd
from sklearn.externals.joblib import Memory
from sklearn.externals.six.moves.urllib.request import urlopen
from sklearn.externals.six import iteritems


print(__doc__)

def index(redirects, index_map, k):
    """Find the index of an article name after redirect resolution"""
    k = redirects.get(k, k)
    return index_map.setdefault(k, len(index_map))


def short_name(nt_uri):
    """Remove the < and > URI markers and the common URI prefix"""
    return nt_uri[SHORTNAME_SLICE]

def get_redirects(redirects_filename):
    """Parse the redirections and build a transitively closed map out of it"""
    redirects = {}
    print("Parsing the NT redirect file")
    for l, line in enumerate(BZ2File(redirects_filename)):
        split = line.split()
        if len(split) != 4:
            print("ignoring malformed line: " + line)
            continue
        redirects[short_name(split[0])] = short_name(split[2])
        if l % 1000000 == 0:
            print("[%s] line: %08d" % (datetime.now().isoformat(), l))

    # compute the transitive closure
    print("Computing the transitive closure of the redirect relation")
    for l, source in enumerate(redirects.keys()):
        transitive_target = None
        target = redirects[source]
        seen = set([source])
        while True:
            transitive_target = target
            target = redirects.get(target)
            if target is None or target in seen:
                break
            seen.add(target)
        redirects[source] = transitive_target
        if l % 1000000 == 0:
            print("[%s] line: %08d" % (datetime.now().isoformat(), l))

    return redirects

def build_fighter_index(fights):
    ind = {}
    next_index = 0
    for fight in fights:
        if not (fight.f0 in ind):
            ind[fight.f0] = next_index
            next_index += 1

        if not (fight.f1 in ind):
            ind[fight.f1] = next_index
            next_index += 1

    return ind

#def get_adjacency_matrix(redirects_filename, page_links_filename, limit=None):
def get_adjacency_matrix(fights):
    fighter_indexes = build_fighter_index(fights)

    X = sparse.lil_matrix((len(fighter_indexes), len(fighter_indexes)),
                          dtype=np.float32)
    for fight in fights:
        if (fight.result == 'win') or (fight.result == 'loss'):
            f0_ind = fighter_indexes[fight.f0]
            f1_ind = fighter_indexes[fight.f1]

            if fight.result == 'win':
                X[f0_ind, f1_ind] = 1.0
            else:
                X[f1_ind, f0_ind] = 1.0

    return X, fighter_indexes

#     """Extract the adjacency graph as a scipy sparse matrix

#     Redirects are resolved first.

#     Returns X, the scipy sparse adjacency matrix, redirects as python
#     dict from article names to article names and index_map a python dict
#     from article names to python int (article indexes).
#     """

#     print("Computing the redirect map")
#     redirects = get_redirects(redirects_filename)

#     print("Computing the integer index map")
#     index_map = dict()
#     links = list()
#     for l, line in enumerate(BZ2File(page_links_filename)):
#         split = line.split()
#         if len(split) != 4:
#             print("ignoring malformed line: " + line)
#             continue
#         i = index(redirects, index_map, short_name(split[0]))
#         j = index(redirects, index_map, short_name(split[2]))
#         links.append((i, j))
#         if l % 1000000 == 0:
#             print("[%s] line: %08d" % (datetime.now().isoformat(), l))

#         if limit is not None and l >= limit - 1:
#             break

#     print("Computing the adjacency matrix")
#     X = sparse.lil_matrix((len(index_map), len(index_map)), dtype=np.float32)
#     for i, j in links:
#         X[i, j] = 1.0
#     del links
#     print("Converting to CSR representation")
#     X = X.tocsr()
#     print("CSR conversion done")
#     return X, redirects, index_map


# # # stop after 5M links to make it possible to work in RAM
# # X, redirects, index_map = get_adjacency_matrix(
# #     redirects_filename, page_links_filename, limit=5000000)
# # names = dict((i, name) for name, i in iteritems(index_map))

# # print("Computing the principal singular vectors using randomized_svd")
# # t0 = time()
# # U, s, V = randomized_svd(X, 5, n_iter=3)
# # print("done in %0.3fs" % (time() - t0))

# # # print the names of the wikipedia related strongest components of the
# # # principal singular vector which should be similar to the highest eigenvector
# # print("Top wikipedia pages according to principal singular vectors")
# # pprint([names[i] for i in np.abs(U.T[0]).argsort()[-10:]])
# # pprint([names[i] for i in np.abs(V[0]).argsort()[-10:]])


# def centrality_scores(X, alpha=0.85, max_iter=100, tol=1e-10):
#     """Power iteration computation of the principal eigenvector

#     This method is also known as Google PageRank and the implementation
#     is based on the one from the NetworkX project (BSD licensed too)
#     with copyrights by:

#       Aric Hagberg <hagberg@lanl.gov>
#       Dan Schult <dschult@colgate.edu>
#       Pieter Swart <swart@lanl.gov>
#     """
#     n = X.shape[0]
#     X = X.copy()
#     incoming_counts = np.asarray(X.sum(axis=1)).ravel()

#     print("Normalizing the graph")
#     for i in incoming_counts.nonzero()[0]:
#         X.data[X.indptr[i]:X.indptr[i + 1]] *= 1.0 / incoming_counts[i]
#     dangle = np.asarray(np.where(X.sum(axis=1) == 0, 1.0 / n, 0)).ravel()

#     scores = np.ones(n, dtype=np.float32) / n  # initial guess
#     for i in range(max_iter):
#         print("power iteration #%d" % i)
#         prev_scores = scores
#         scores = (alpha * (scores * X + np.dot(dangle, prev_scores))
#                   + (1 - alpha) * prev_scores.sum() / n)
#         # check convergence: normalized l_inf norm
#         scores_max = np.abs(scores).max()
#         if scores_max == 0.0:
#             scores_max = 1.0
#         err = np.abs(scores - prev_scores).max() / scores_max
#         print("error: %0.6f" % err)
#         if err < n * tol:
#             return scores

#     return scores

# # print("Computing principal eigenvector score using a power iteration method")
# # t0 = time()
# # scores = centrality_scores(X, max_iter=100, tol=1e-10)
# # print("done in %0.3fs" % (time() - t0))
# # pprint([names[i] for i in np.abs(scores).argsort()[-10:]])
