import numpy as np
import itertools
import pymcdm
import pymcdm.methods as methods

def generate_criteria_index_sets(matrix, min_crit=2):
    S = []
    # generate vector of criteria indexes
    criteria_set = np.arange(0, matrix.shape[1], 1)
    # generate sets of criteria indexes (S)
    for i in range(min_crit, matrix.shape[1]+1):
        S.extend(list(itertools.combinations(criteria_set, i)))
    return S

def generate_modifications_sets(B, S, step=1):
    M, modification_steps = [], []
    # for each modification bound (B) generate vector of modification sizes
    for b in B:
        modification_steps.append(np.arange(0, b+1))
    # for each set of criteria indexes (S) generate a cartesian product of modification sizes (M)
    for index_set in S:
        M.append(list(itertools.product(*[modification_steps[i] for i in index_set])))
    return M

def get_interval_prefs(matrix, weights, criteria_types, bounds, step=1):
    S = generate_criteria_index_sets(matrix)
    M = generate_modifications_sets(bounds, S, step)
    
    topsis = methods.TOPSIS(normalization_function=pymcdm.normalizations.max_normalization)
    
    interval_pref = []
    # examine each alternative
    for i in range(matrix.shape[0]):
        alt_pref = []
        # modify matrix for each criteria index set and modifications
        for crit_indexes, modification_set in zip(S, M):
            for single_modification in modification_set:
                # copy initial matrix
                npmatrix = matrix.copy()
                nmmatrix = matrix.copy()

                # modify matrix for criteria indexes by increasing and decreasing
                for j, mod_val in zip(crit_indexes, single_modification):
                    npmatrix[i, j] = matrix[i, j] + matrix[i, j] * (mod_val/100)
                    nmmatrix[i, j] = matrix[i, j] - matrix[i, j] * (mod_val/100)

                # assess matrices after changes
                nppref = topsis(npmatrix, weights, criteria_types)
                nmpref = topsis(nmmatrix, weights, criteria_types)

                # save preferences of alternatives
                alt_pref.extend([nppref[i], nmpref[i]])
        if i == 0:
            print(alt_pref[0], alt_pref[1], alt_pref[2], alt_pref[-3], alt_pref[-2], alt_pref[-1])
                
        # save minimum and maximum preference scores as interval preference 
        interval_pref.append([np.min(alt_pref), np.max(alt_pref)])
    
    return interval_pref

if __name__ == '__main__':
    # Example usage
    # initial data
    matrix = np.array([
        [3.15, 2.29, 1.81, 4.67],
        [3.20, 2.42, 1.82, 4.83],
        [3.24, 2.33, 1.90, 4.45],
        [3.11, 2.11, 1.99, 4.59],
        [3.30, 2.26, 1.70, 4.72],
    ])

    weights = np.array([0.33, 0.24, 0.16, 0.27])
    criteria_types = np.array([-1, 1, -1, 1])
    modifications = np.array([5, 4, 3, 4])

    # interval preferences from COMSAM method
    interval_preferences = get_interval_prefs(matrix, weights, criteria_types, modifications)
    print(interval_preferences)