from math import pi, cos, sin
import numpy as np

# A few variables just to help clean the code up
zMat = np.array([[0, 0]])

# Constant arrays for defining connectivity matrices
e1 = np.array([[1, 0]])
e2 = np.array([[0, 1]])
E1 = np.concatenate( (e1, zMat) )
E2 = np.concatenate( (zMat, e2) )
T1 = np.concatenate( (zMat, zMat, e2, np.negative(e2), np.negative(e2), zMat, zMat, np.negative(e2)) ) # Capital Theta 1
T2 = np.concatenate( (e2, np.negative(e1), np.negative(e2), zMat, e1, e2, np.negative(e1), zMat, zMat) ) # Capital Theta 2
T3 = np.concatenate( (zMat, zMat, zMat, zMat, zMat, zMat, np.negative(e1), e2) ) # Capital Theta 3
T4 = np.concatenate( (zMat, e1, np.negative(e1), zMat, zMat, e1, e1, zMat) ) # Capital Theta 4

class N:
    Nl = None

    def __init__(self, i, k, R, r, p, q):
        for l in range(1, 3):
            # The angles
            phil = (2 * i + (l - 1)) * (pi / q)
            thetal = (2 * k + l) * (pi / p)

            # The torus radii
            Rl = np.array([R * cos(phil), R * sin(phil), 0])
            rl = np.array([r * cos(thetal) * cos(phil),
                        r * cos(thetal) * sin(phil),
                        -r * sin(thetal)])

            rs_added = np.add(Rl, rl)

            # Either start the array off, or dstack the two 1D arrays together into a 2D array
            if l == 1:
                self.Nl = np.array(rs_added)
            else:
                self.Nl = np.dstack((self.Nl, rs_added))

        return None

    def get(self):
        return self.Nl
