import pandas as pd
import numpy as np
import math

def conditional_mutual_information_test(data:pd.DataFrame, X:set, Y:set, Z:set = None, alpha:float = 0.05, delta:float = None) -> bool:
    def conditional_mutual_information(data, X:set, Y:set, Z:set):
        X = list(X); Y = list(Y); Z = list(Z)
        cmi = 0

        P_Z = data.groupby(Z).size()
        P_Z = P_Z/P_Z.sum()

        P_XZ = data.groupby(X + Z).size()
        P_XZ = P_XZ/P_XZ.sum()

        P_YZ = data.groupby(Y + Z).size()
        P_YZ = P_YZ/P_YZ.sum()

        P_XYZ = data.groupby(X + Y + Z).size()
        P_XYZ = P_XYZ/P_XYZ.sum()

        for ind in P_XYZ.index:
            x_ind = ind[:len(X)]
            y_ind = ind[len(X):len(X + Y)]
            z_ind = ind[len(X + Y):]

            xz_ind = x_ind + z_ind
            yz_ind = y_ind + z_ind
            xyz_ind = ind

            z_ind =  pd.MultiIndex.from_tuples([z_ind], names = Z) if len(Z) != 1 else pd.Index(z_ind, name = Z[0])
            xz_ind = pd.MultiIndex.from_tuples([xz_ind], names = X + Z)
            yz_ind = pd.MultiIndex.from_tuples([yz_ind], names = Y + Z)
            xyz_ind = pd.MultiIndex.from_tuples([xyz_ind], names = X + Y + Z)

            cmi += delta * P_XYZ[xyz_ind].item() * np.log2(P_Z[z_ind].item() * P_XYZ[xyz_ind].item() / (P_XZ[xz_ind].item() * P_YZ[yz_ind].item()))

        return cmi
    
    def mutual_information(data, X:set, Y:set):
        X = list(X); Y = list(Y)
        mi = 0

        P_X = data.groupby(X).size()
        P_X = P_X/P_X.sum()

        P_Y = data.groupby(Y).size()
        P_Y = P_Y/P_Y.sum()
        

        P_XY = data.groupby(X + Y).size()
        P_XY = P_XY/P_XY.sum()


        for ind in P_XY.index:
            x_ind = ind[:len(X)]
            y_ind = ind[len(X):]
            xy_ind = [ind]

            x_ind =  pd.MultiIndex.from_tuples([x_ind], names = X) if len(X) != 1 else pd.Index(x_ind, name = X[0])
            y_ind =  pd.MultiIndex.from_tuples([y_ind], names = Y) if len(Y) != 1 else pd.Index(y_ind, name = Y[0])
            xy_ind = pd.MultiIndex.from_tuples(xy_ind, names = X + Y)

            mi += delta * P_XY[xy_ind].item() * np.log2(P_XY[xy_ind].item()/(P_X[x_ind].item() * P_Y[y_ind].item()))

        return mi

    if delta is not None:
      data = data.copy().round(-math.floor(np.log10(delta)))
    else: delta = 1

    if Z:
        mi = conditional_mutual_information(data, X, Y, Z)
    else:
        mi = mutual_information(data, X, Y)
    
    return mi < alpha