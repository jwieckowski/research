import numpy as np
from Interval_TOPSIS import INTERVAL_TOPSIS as itopsis
from pymcdm.weights import entropy_weights
from pymcdm.helpers import rankdata
from methods import *

np.set_printoptions(suppress=True, precision=4)


# decision matrix presented in the article
matrix = np.array([
    [161000, 6.9, 385, 690, 90, 157, 17.8, 62, 217, 1727, 340],
    [145400, 9.5, 395, 565, 65, 135, 13.0, 52, 110, 1502, 225],
    [330000, 3.2, 652, 660, 45, 250, 18.8, 85, 320, 2162, 441],
    [130400, 9.0, 444, 900, 30, 150, 14.3, 37, 118, 1440, 220],
    [308000, 5.7, 417, 540, 90, 200, 23.2, 95, 408, 2565, 664],
    [169700, 7.2, 300, 660, 42, 150, 17.2, 33, 170, 1195, 250],
    [139000, 9.0, 324, 252, 30, 150, 17.8, 50, 136, 1523, 260],
])

# criteria types for the considered set of criteria
criteria_types = ['cost', 'cost', 'profit', 'cost',
                          'cost', 'profit', 'cost', 'profit', 'profit', 'cost', 'profit']

# weights calculated by the entropy method
weights = entropy_weights(matrix)

# matrix of intervals representing the interval spread
# for purpose of calculating the initial ranking, all values are set to 1
interval_ranges = np.array([[[1, 1] for c in range(matrix.shape[1])]
                            for r in range(matrix.shape[0])])

# step of interval blurring
STEP = 0.01

# calculating crisp ranking for the TOPSIS method
topsis = itopsis(matrix, criteria_types, weights, interval_ranges)
topsis.run()
crisp_ranking = rankdata(topsis.preferences, reverse=True)

print('CRISP TOPSIS RESULTS')
print(f'Preferences: {topsis.preferences}')
print(f'Ranking: {crisp_ranking}')

SHOW_FIGURES = True

# APPROACH 1
print('\nALL CRITERIA ONE ALTERNATIVE APPROACH')
alternative_sensitivity = all_criteria_one_alternative(
    matrix, weights, criteria_types, crisp_ranking, SHOW_FIGURES)

for index, sens in enumerate(alternative_sensitivity):
    print(f'Alternative {index+1}: {sens}')

# APPROACH 2
print('\nONE CRITERION ALL ALTERNATIVES APPROACH')
criteria_sensitivity = one_criterion_all_alternatives(
    matrix, weights, criteria_types, crisp_ranking, SHOW_FIGURES)

for index, sens in enumerate(criteria_sensitivity):
    print(f'Criterion {index+1}: {sens}')

# Because of the complexity of the problem, third ans fourth approach need a few minuted to proceed to provide output

# APPROACH 3
print('\nONE CRITERION ONE ALTERNATIVE APPROACH')
alternative_criteria_sensitivity = one_criterion_one_alternative(
    matrix, weights, criteria_types, crisp_ranking, SHOW_FIGURES)

for alt_index, alt_sens in enumerate(alternative_criteria_sensitivity):
    print(f'Alternative {alt_index+1}')
    for crit_index, crit_sens in enumerate(alt_sens):
        print(f'Criterion {crit_index+1}: {crit_sens}')
    print('')

# APPROACH 4
print('\nSET OF CRITERIA ONE ALTERNATIVE APPROACH')
rankings_change_dict = set_criteria_one_alternative(
    matrix, weights, criteria_types, crisp_ranking)

sorted_rankings_change_dict = sort_ranking_dictionary_by_changes(
    rankings_change_dict, 10)

for item in sorted_rankings_change_dict:
    elements = item[0].split('_')
    alternative = elements[1]
    criteria_indexes = ' '.join(elements[3:])
    criteria_sensitivity = item[1]['changes']
    print(f'Alternative: {alternative}')
    print(f'Criteria set: {criteria_indexes}')
    print(f'Criteria sensitivity: {criteria_sensitivity}')
    print('')
