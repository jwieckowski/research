import numpy as np

def fRANCOM(ranking, explain=False):
    """Calculate criteria fuzzy weights based on the given order of criteria importance. Lower values in ranking mean higher relevance.

    Parameters
    ----------
        ranking : ndarray
            Numerical values for criteria relevance (lower - more relevant)
        
        explain : boolean, default=False
            Flag showing if partial results will be displayed

    Returns
    -------
        ndarray
            Triangular fuzzy weights
    """

    def f(r1, r2):     
        if r1 < r2:
            return 1
        if r1 == r2:
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

    def toTFN(mac):
        fmac = np.zeros((mac.shape[0], mac.shape[1], 3))
        fmac[mac == 0] = [0, 0, 0.5]
        fmac[mac == 0.5] = [0, 0.5, 1]
        fmac[mac == 1] = [0.5, 1, 1]
        return fmac

    def norm(scw):
        fscw = scw / np.sum(scw, axis=0)[1]
        return fscw

    def get_weights(ranking):
        mac = build_mac(ranking)

        fmac = toTFN(mac)
        fscw = np.sum(fmac, axis=1)

        p = norm(fscw)

        if explain:
            print('Matrix of ranking Comparison (MAC)')
            print(mac)
            print('')
            print('Triangular Fuzzy Number MAC')
            print(toTFN(mac))
            print('')
            print('Fuzzy Summed Criteria Weights')
            print(fscw)
            print('')

        return p

    return get_weights(ranking)



if __name__ == "__main__":
    # Usage example
    rank = np.array([1, 2, 3])
    weights = fRANCOM(rank)
    print(weights)


