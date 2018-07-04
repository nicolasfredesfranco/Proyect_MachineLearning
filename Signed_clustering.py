import numpy as np
from sklearn.utils.extmath import _deterministic_vector_sign_flip
from sklearn.utils import check_random_state
from scipy.sparse.linalg import eigsh
from sklearn.cluster.spectral import discretize  

def _setdiag_dense(A, d):
    A.flat[::len(d)+1] = d

def signed_laplacian(affinity):

    m = np.array(affinity,dtype='float')
    np.fill_diagonal(m, 0)
    w=np.absolute(m)
    w=w.sum(axis=0)
    isolated_node_mask = (w == 0)
    w = np.where(isolated_node_mask, 1, np.sqrt(w))
    m /= w
    m /= w[:, np.newaxis]
    m *= -1
    _setdiag_dense(m, 1 - isolated_node_mask)
    return m, w

def signal_spectral_embedding(affinity,random_state=None,n_clusters=2,eigen_tol=0.0):


    """
    affinity: Matriz de pesos del grafo.    
    random_state: fija la semilla para check random state.
    n_cluster:cantidad de clusters.
    tol: se requiere para eigsh.
    """
    random_state=check_random_state(random_state)

    laplacian, dd = signed_laplacian(affinity)
    laplacian *= -1
    v0 = random_state.uniform(-1, 1, laplacian.shape[0])
    lambdas, diffusion_map = eigsh(laplacian, k=n_clusters,
                               sigma=1.0, which='LM',
                               tol=eigen_tol, v0=v0)
    embedding = diffusion_map.T[n_clusters::-1] * dd

    # modifica el signo de los vectores para reproducibilidad.
    embedding=_deterministic_vector_sign_flip(embedding)
    return embedding[:n_clusters].T

def signal_spectral_clustering(affinity,random_state=None,n_clusters=2,eigen_tol=0.0):

    maps=signal_spectral_embedding(affinity,random_state,n_clusters,eigen_tol)
    clusters=discretize(maps,random_state=random_state)
    return clusters    
        

