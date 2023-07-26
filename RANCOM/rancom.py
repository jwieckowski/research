import numpy as np

def RANCOM(ranking):
    """Calculate criteria weights based on the given numerical hierarchy.

    Parameters
    ----------
        ranking : ndarray
            Numerical values for criteria relevance (lower - more relevant).

    Returns
    -------
        ndarray
            Criteria weights in range 0-1.
    """

    def f(c1, c2):
        if c1 < c2:
            return 1
        if c1 == c2:
            return 0.5
        return 0

    def build_mac(ranking):
        co = np.array(list(ranking))

        mac = np.diag(np.ones(co.shape[0]) * 0.5)
        for i in range(mac.shape[0]):
            for j in range(i+1, mac.shape[1]):
                v = f(co[i], co[j])
                mac[i, j] = v
                mac[j, i] = 1 - v
        return mac

    def get_preference(ranking):
        mac = build_mac(ranking)
        scw = np.sum(mac, axis=1)

        macSum = np.sum(scw)
        p = np.zeros(scw.shape[0], dtype=float)
        for i in range(0, scw.shape[0]):
            p[i] = scw[i] / macSum
        return p

    return get_preference(ranking)


if __name__ == "__main__":
    rank = np.array([1, 2])
    r1 = RANCOM(rank)
    print(r1)
