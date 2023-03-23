import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.spatial.distance import pdist, squareform

def gaussian_kernel(data:pd.DataFrame, X:set, sigma:float = None, unit_variance:bool = False) -> np.array:
    X = data.loc[:, list(X)].to_numpy()#.transpose()
    if not unit_variance:
        X = X/X.std(axis=0)

    # from https://stats.stackexchange.com/questions/15798/how-to-calculate-a-gaussian-kernel-effectively-in-numpy
    dist = squareform(pdist(X, 'euclidean'))
    if not sigma : 
      n = len(dist)
      sigma = np.median(dist[np.triu_indices(n, k = 1)])
    K = np.exp(-dist**2/ (2*sigma**2))
    return K

def centralized_gaussian_kernel(data:pd.DataFrame, X:set, sigma:float = None, unit_variance:bool = False) -> np.array:
    K = gaussian_kernel(data, X, sigma, unit_variance)
    n = len(K)
    H = np.identity(n) - np.ones((n, n))/n
    return np.matmul(np.matmul(H, K), H)

def kcit(data:pd.DataFrame, X:set, Y:set, Z:set = None, regulation:float = 1e-3, alpha:float = 0.05,  unit_variance:bool = False, log10 = False, **test_kwarg) -> bool:
    # hyper parameter setting
    hyper_parameter = dict()

    if len(data) < 200: hyper_parameter['width'] = 0.8
    elif len(data) > 1200: hyper_parameter['width'] = 0.3
    else: hyper_parameter['width'] = 0.5 

    for kw, value in test_kwarg.items():
        hyper_parameter[kw] = value

    n = len(data)
    # Independence Test
    if Z is None:
        Kx = centralized_gaussian_kernel(data, X, unit_variance)
        Ky = centralized_gaussian_kernel(data, Y, unit_variance)

        T = np.matmul(Kx, Ky).trace() / n
        E_T = Kx.trace() * Ky.trace() / (n**2)
        V_T = 2 * np.matmul(Kx, Kx).trace() * np.matmul(Ky, Ky).trace() / (n**4)

        k = E_T**2 / V_T
        theta = V_T/E_T 
    
    else:
        # X = [X, Z]
        X = X|Z

        # Kx, Ky, Kz <- centralized kernel matrix of X, Y, Z with hyper_parameter['width']
        Kx = centralized_gaussian_kernel(data, X, hyper_parameter['width'])
        Ky = centralized_gaussian_kernel(data, Y, hyper_parameter['width'])
        Kz = centralized_gaussian_kernel(data, Z, hyper_parameter['width'])
        
        Rz = regulation * np.linalg.inv(Kz + regulation * np.identity(n))
        Kxz = np.matmul(np.matmul(Rz, Kx), Rz)
        Kyz = np.matmul(np.matmul(Rz, Ky), Rz)

        Lxz, Vx = np.linalg.eig(Kxz)
        Lyz, Vy = np.linalg.eig(Kyz)

        # soring eigenvalues and corresponding eigenvectors
        idx = Lxz.argsort()
        Lxz, Vx = Lxz[idx], np.real(Vx[:, idx])
        idx = Lyz.argsort()
        Lyz, Vy = Lyz[idx], np.real(Vy[:, idx])

        # diag(Vx(Vy.T))
        W = np.zeros(n)
        for t in range(n):
            W[t] = np.inner(Vx[t], Vy[t])

        # W = W(W.T)
        W = np.asmatrix(W)
        W = np.matmul(W, W.transpose())

        T = np.matmul(Kxz, Kyz).trace().item()/n
        E_T = W.trace().item()/n
        V_T = 2 * np.matmul(W, W).trace().item()/(n**2)
    
        k = E_T**2 / V_T
        theta = 1/np.log10(E_T/V_T) if log10 else V_T/E_T

    cri = stats.gamma(a = k, scale = theta).ppf(1 - alpha)
    
    return T < cri