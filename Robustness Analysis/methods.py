import numpy as np
from Interval_TOPSIS import INTERVAL_TOPSIS as itopsis
from pymcdm.helpers import rankdata
import itertools
import matplotlib.pyplot as plt

# method to create interval based on the step and criterion type


def create_interval(interval_step, index, criteria_types):
    interval = [
        1, 1 + interval_step] if criteria_types[index] == 'profit' else [1 - interval_step, 1]
    return interval

# method to sort dictionary by changes in rankings
# use when dealing with fourth approach and want to get the most variable rankings


def sort_ranking_dictionary_by_changes(rankings_change, N):
    sorted_dict = sorted(rankings_change.items(),
                         key=lambda x: x[1]['counter'], reverse=True)[0:N]
    return sorted_dict

# first approach described in article
# interval blurr for all criteria and one alternative


def all_criteria_one_alternative(matrix, weights, criteria_types, crisp_ranking, show_figure=False, STEP=0.01):
    alternatives_sensitivity = [[] for i in range(matrix.shape[0])]

    for alt in range(matrix.shape[0]):

        alt_rankings = []
        last_ranking = crisp_ranking

        for i in range(1, 100):
            current_interval_step = np.round(STEP * i, 2)
            current_interval_ranges = np.array([[create_interval(current_interval_step, c, criteria_types) if r == alt else [1, 1]
                                                for c in range(matrix.shape[1])] for r in range(matrix.shape[0])])

            it = itopsis(matrix, criteria_types, weights,
                         current_interval_ranges)
            it.run()
            interval_ranking = rankdata(it.preferences, reverse=True)

            alt_rankings.append(list(interval_ranking))

            if not np.array_equal(interval_ranking, last_ranking):
                alternatives_sensitivity[alt].append(current_interval_step)

            last_ranking = interval_ranking

        if show_figure == True:
            alt_labels = ['A' + str(i + 1) for i in range(matrix.shape[0])]

            alt_rankings = np.array(alt_rankings).T
            x = np.linspace(1, 100, len(alt_rankings[0]))
            y = [i+1 for i in range(matrix.shape[0])]
            for idx, rank in enumerate(alt_rankings):
                plt.plot(x, rank, label=alt_labels[idx])
            plt.ylabel('Ranking position', fontsize=14)
            plt.xlabel('Interval percentage range', fontsize=14)
            plt.grid(alpha=0.5, linestyle='--', linewidth=1)
            plt.legend(bbox_to_anchor=(1.04, 0.5),
                       loc="lower left", borderaxespad=0)
            plt.title(f'Interval blur for alternative A{alt+1}', fontsize=16)
            plt.tight_layout()
            plt.show()

    return alternatives_sensitivity

# second approach described in article
# interval blurr for one criterion and all alternatives


def one_criterion_all_alternatives(matrix, weights, criteria_types, crisp_ranking, show_figure=False, STEP=0.01):
    criteria_sensitivity = [[] for i in range(matrix.shape[1])]

    for crit in range(matrix.shape[1]):

        crit_rankings = []
        last_ranking = crisp_ranking

        for i in range(1, 100):
            current_interval_step = np.round(STEP * i, 2)
            current_interval_ranges = np.array([[create_interval(current_interval_step, c, criteria_types) if c == crit else [1, 1]
                                                for c in range(matrix.shape[1])] for r in range(matrix.shape[0])])

            it = itopsis(matrix, criteria_types, weights,
                         current_interval_ranges)
            it.run()

            interval_ranking = rankdata(it.preferences, reverse=True)
            crit_rankings.append(list(interval_ranking))

            if not np.array_equal(interval_ranking, last_ranking):
                criteria_sensitivity[crit].append(current_interval_step)

            last_ranking = interval_ranking

        if show_figure == True:
            alt_labels = ['A' + str(i + 1) for i in range(matrix.shape[0])]

            crit_rankings = np.array(crit_rankings).T
            x = np.linspace(1, 100, len(crit_rankings[0]))
            y = [i+1 for i in range(matrix.shape[0])]
            for idx, rank in enumerate(crit_rankings):
                plt.plot(x, rank, label=alt_labels[idx])
            plt.ylabel('Ranking position', fontsize=14)
            plt.xlabel('Interval percentage range', fontsize=14)
            plt.grid(alpha=0.5, linestyle='--', linewidth=1)
            plt.legend(bbox_to_anchor=(1.04, 0.5),
                       loc="lower left", borderaxespad=0)
            plt.title(
                f'Interval blur for criterion C{crit+1}', fontsize=16)
            plt.tight_layout()
            plt.show()

    return criteria_sensitivity

# third approach described in article
# interval blurr for one criterion and one alternative


def one_criterion_one_alternative(matrix, weights, criteria_types, crisp_ranking, show_figure=False, STEP=0.01):
    alternatives_criteria_sensitivity = [
        [[] for j in range(matrix.shape[1])] for i in range(matrix.shape[0])]

    for alt in range(matrix.shape[0]):
        for crit in range(matrix.shape[1]):

            alt_crit_rankings = []
            last_ranking = crisp_ranking

            for i in range(1, 100):
                current_interval_step = np.round(STEP * i, 2)
                current_interval_ranges = np.array([[create_interval(current_interval_step, c, criteria_types) if c == crit and r == alt else [1, 1]
                                                    for c in range(matrix.shape[1])] for r in range(matrix.shape[0])])

                it = itopsis(matrix, criteria_types, weights,
                             current_interval_ranges)
                it.run()

                interval_ranking = rankdata(it.preferences, reverse=True)
                alt_crit_rankings.append(list(interval_ranking))

                if not np.array_equal(interval_ranking, last_ranking):
                    alternatives_criteria_sensitivity[alt][crit].append(
                        current_interval_step)

                last_ranking = interval_ranking

            if show_figure == True:
                alt_labels = ['A' + str(i + 1)
                              for i in range(matrix.shape[0])]

                alt_crit_rankings = np.array(alt_crit_rankings).T
                x = np.linspace(1, 100, len(alt_crit_rankings[0]))
                y = [i+1 for i in range(matrix.shape[0])]
                for idx, rank in enumerate(alt_crit_rankings):
                    plt.plot(x, rank, label=alt_labels[idx])
                plt.ylabel('Ranking position', fontsize=14)
                plt.xlabel('Interval percentage range', fontsize=14)
                plt.grid(alpha=0.5, linestyle='--', linewidth=1)
                plt.legend(bbox_to_anchor=(1.04, 0.5),
                           loc="lower left", borderaxespad=0)
                plt.title(
                    f'Interval blur for alternative A{alt+1} and criterion C{crit+1}', fontsize=16)
                plt.tight_layout()
                plt.show()

    return alternatives_criteria_sensitivity


# fourth approach described in article
# interval blurr for set of criteria and one alternative
def set_criteria_one_alternative(matrix, weights, criteria_types, crisp_ranking, STEP=0.01):
    rankings_change = {}

    crit_indexes = np.arange(0, matrix.shape[1], 1)
    for s in range(2, matrix.shape[1]-1):
        all_comb = itertools.combinations(crit_indexes, s)
        for comb in all_comb:
            current_crit_indexes = list(comb)

            for alt in range(matrix.shape[0]):

                crit_str = '_'.join(map(str, current_crit_indexes))
                key = f'A_{alt}_C_{crit_str}'
                rankings_change[key] = {}
                rankings_change[key]['counter'] = 0
                rankings_change[key]['rankings'] = []
                rankings_change[key]['changes'] = []

                last_ranking = crisp_ranking

                for i in range(1, 100):
                    current_interval_step = np.round(STEP * i, 2)
                    current_interval_ranges = np.array([[create_interval(current_interval_step, c, criteria_types) if c in current_crit_indexes and r == alt else [1, 1]
                                                        for c in range(matrix.shape[1])] for r in range(matrix.shape[0])])

                    it = itopsis(matrix, criteria_types, weights,
                                 current_interval_ranges)
                    it.run()

                    interval_ranking = rankdata(it.preferences, reverse=True)

                    if not np.array_equal(interval_ranking, last_ranking):
                        rankings_change[key]['counter'] += 1
                        rankings_change[key]['changes'].append(
                            current_interval_step)
                        last_ranking = interval_ranking

                    rankings_change[key]['rankings'].append(
                        list(interval_ranking))

    return rankings_change
