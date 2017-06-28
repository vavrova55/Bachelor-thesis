import numpy as np
from decimal import Decimal, ROUND_HALF_UP

class ModularInverse:
    def __init__(self, matrix, lenght):
        self.key = matrix
        self.n = lenght
        determinant = np.linalg.det(self.key)
        det = int(Decimal(round(determinant, 1)).quantize(0, rounding=ROUND_HALF_UP))

        if det == 0:
            return

        self.inverseKey = np.linalg.inv(self.key)
        self.resultRight = det * self.inverseKey

        det = self.remake(det)
        if det == 0:
            self.result = None
            return

        self.vypis(det)

    def extendedEuclid(self, a, b):
        pole = []
        if (b == 0):
            # if b =0, then return g =a, m=1, n=0
            # print(a, "\t", b, "\t", a, "\t", 1, "\t", 0)
            return (a, 1, 0)
        else:
            # if b is not 0, then recursively call the function to get the value of
            # g,m,n at each step. The code also displays the value of a,b at each step
            (g, m, n) = self.extendedEuclid(b, a % b)
            # print(a, "\t", b, "\t", g, "\t", n, "\t", m - (a // b) * n)
            pole.append([g, n, m - (a // b) * n])
            return (g, n, m-(a//b)*n)


    def vypis(self, det):
        x = self.extendedEuclid(self.n, det)[-1]
        x = self.remake(x)

        modInverse = x*self.resultRight

        # upravim cisla pri mod self.n a prevediem ich z typu np.float64 na zaokruhlene cele cislo
        result = []
        for i in modInverse:
            tmp = []
            for j in i:
                x = self.remake(j)
                tmp.append(int(Decimal(round(x, 1)).quantize(0, rounding=ROUND_HALF_UP)))
            result.append(tmp)
        self.result = np.array(result)

        return result

    def remake(self, value, mod=47):
        if value >= mod:
            while value >= mod:
                value -= mod
        elif value < 0:
            while value < 0:
                value += mod
        return value

    def getResult(self):
        return self.result
