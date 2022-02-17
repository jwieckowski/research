import numpy as np
import copy


class INTERVAL_TOPSIS:
    def __init__(self, matrix, types, weights, matrixRange):
        self.matrix = matrix
        self.types = types
        self.weights = weights
        self.matrixRange = matrixRange

    def create_interval(self):
        """
        creates a matrix with interval values based on given ranges
        :return: interval matrix
        """
        row, col = self.matrix.shape
        self.interval_matrix = np.array([[[self.matrix[r][c] * self.matrixRange[r][c][0], self.matrix[r]
                                        [c] * self.matrixRange[r][c][1]] for c in range(col)] for r in range(row)])

    def normalize_matrix(self):
        """
        normalize interval matrix
        :return: normalized interval matrix
        """
        row, col, l = self.interval_matrix.shape
        self.normalized_matrix = copy.deepcopy(self.interval_matrix)
        for c in range(col):
            d = np.sqrt(
                np.sum(np.array(self.interval_matrix[:, c]**2).flatten()))
            self.normalized_matrix[:, c] = self.interval_matrix[:, c] / d

    def weights_multiply(self):
        """
        multiply every interval value in matrix by the weight for criteria
        :return: weighted normalized decision matrix
        """
        self.weighted_normalized_matrix = copy.deepcopy(self.normalized_matrix)
        row, col, l = self.normalized_matrix.shape
        for c in range(col):
            self.weighted_normalized_matrix[:,
                                            c] = self.normalized_matrix[:, c] * self.weights[c]

    def calculate_distance(self):
        """
        calculate positive and negative distances from ideal solution
        :return: two lists of positive and negative distance from ideal solution
        """

        self.PIS = []
        self.NIS = []

        for t in self.types:
            if t == 'profit':
                self.PIS.append(
                    np.max(self.weighted_normalized_matrix[:, self.types.index(t)]))
                self.NIS.append(
                    np.min(self.weighted_normalized_matrix[:, self.types.index(t)]))
            else:
                self.PIS.append(
                    np.min(self.weighted_normalized_matrix[:, self.types.index(t)]))
                self.NIS.append(
                    np.max(self.weighted_normalized_matrix[:, self.types.index(t)]))

        self.DP, self.DN = [], []
        row, col, l = self.weighted_normalized_matrix.shape
        for r in range(row):
            self.DP.append(np.sqrt(np.sum((self.weighted_normalized_matrix[r, :][:, 0] - self.PIS)**2) + np.sum(
                (self.weighted_normalized_matrix[r, :][:, 1] - self.PIS)**2)))
            self.DN.append(np.sqrt(np.sum((self.weighted_normalized_matrix[r, :][:, 0] - self.NIS)**2) + np.sum(
                (self.weighted_normalized_matrix[r, :][:, 1] - self.NIS)**2)))

    def calculate_preferences(self):
        """
        calculate ranking based on calculated distances
        :return: ranking of alternatives
        """
        self.preferences = []
        for dn, dp in zip(self.DN, self.DP):
            self.preferences.append(dn / (dn + dp))

        self.preferences = np.array(self.preferences, dtype=float)

    def run(self):
        r1, c1 = self.matrix.shape
        r2, c2, i = self.matrixRange.shape
        if r1 != r2 or c1 != c2:
            raise IndexError(
                'Shapes of matrix and range matrix must be the same')
        self.create_interval()
        self.normalize_matrix()
        self.weights_multiply()
        self.calculate_distance()
        self.calculate_preferences()
