import rescomp as rc
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
#from rescomp import optimizer as rcopt
from scipy import sparse
import pydot
#from rescomp.optimizer.optimizer_functions import get_vptime

''' Utilities to quickly get data and iterate
'''

# Functions from DJ's repo #
def remove_edges(A,nedges):
    """ Randomly removes 'nedges' edges from a sparse matrix 'A'
    """
    A = A.todok()
    # Remove Edges
    keys = list(A.keys())

    remove_idx = np.random.choice(range(len(keys)),size=nedges, replace=False)
    remove = [keys[i] for i in remove_idx]
    for e in remove:
        A[e] = 0
    return A

def nrmse(true, pred):
    """ Normalized root mean square error. (A metric for measuring difference in orbits)
    Parameters:
        Two mxn arrays. Axis zero is assumed to be the time axis (i.e. there are m time steps)
    Returns:
        err (ndarray): Error at each time value. 1D array with m entries
    """
    sig = np.std(true, axis=0)
    err = np.linalg.norm((true-pred) / sig, axis=1, ord=2)
    return err

def valid_prediction_index(err, tol):
    """First index i where err[i] > tol. err is assumed to be 1D and tol is a float. If err is never greater than tol, then len(err) is returned."""
    mask = np.logical_or(err > tol, ~np.isfinite(err))
    if np.any(mask):
        return np.argmax(mask)
    return len(err)

def get_vptime(ts, Uts, pre, vpttol=0.5):
    err = nrmse(Uts, pre)
    idx = valid_prediction_index(err, vpttol)
    if idx == 0:
        return 0.
    return ts[idx-1] - ts[0]

#def get_vptime(system, ts, Uts, pre, vpttol=0.5):
#    """
#    Valid prediction time for a specific instance.
#    """
#    err = nrmse(Uts, pre)
#    idx = valid_prediction_index(err, vpttol)
#    if idx == 0:
#        vptime = 0.
#    else:
#        if system.is_driven:
#            vptime = ts[0][idx-1] - ts[0][0]
#        else:
#            vptime = ts[idx-1] - ts[0]

#    return vptime
# ----- #

# Function to save a graph as a .dot file #
def save_as_dot(G,filename):
    #graph = pydot.Dot()
    #graph.set_node_defaults(style="filled", fillcolor="black")
    graph = nx.drawing.nx_pydot.to_pydot(G)
    graph.write_raw(filename)

def generate_thinned_network(n,p_thin,args,topo='Erdos-Reyni'):
    '''
    '''
    if topo == 'Erdos-Reyni':
        p = args[0]
        A = nx.erdos_renyi_graph(n,p,directed=True)
    elif topo == 'RandomGeometric':
        radius = args[0]
        A = nx.random_geometric_graph(n,radius)
    elif topo == 'Barabasi-Albert':
        m = args[0]
        A = nx.barabasi_albert_graph(n,m)
    elif topo == 'Watts-Strogatz':
        k,p = args[0],args[1]
        A = nx.barabasi_albert_graph(n,k,p)

    A = sparse.dok_matrix(nx.adj_matrix(A).T)
    nedges = int(np.floor(p_thin * n))
    A = remove_edges(A,nedges)

    return A


def get_components(A):
    G = nx.DiGraph(A.tocoo())
    weak_components = nx.weakly_connected_components(G)
    return [G.subgraph(c).copy() for c in sorted(weak_components, key=len, reverse=True)]

def get_response(res,ts,Uts):
    r0 = res.r0
    states = res.internal_state_response(ts,Uts,r0)
    X = (res.res+res.W_in@res.W_out)
    response_scaled = np.abs(X@states.T)
    return response_scaled # / np.abs(np.sum(X,axis=1))
