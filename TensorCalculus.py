import numpy as np
import string


def printIndicies(a, n, m, state):
    # if state is equal too True then we do contravariant and if False we do covariant
    letters = list(string.ascii_lowercase)
    if state:
        a += "^("
    else:
        a += "_("
    for i in range(m, n + m):
        a += letters[i]
    a += ")"
    return a


class tensor:
    def __init__(self, dim, sig, type, coeficents):
        # Dimensionality of the manifold : int > 0
        self.dim = dim

        # Signature of the manifold: tuple (int,int)
        if len(sig) != dim:
            raise ValueError("Signature must be the same length as the dimensionality -- dim: " + str(
                dim) + "  length of signature: " + str(len(sig)))
        self.sig = sig

        # Number of tensor product copies of tangent and cotangent space:
        # tuple type[0] = tangent or number of contravariant indecies and type[1] = cotangent or number of covariant indecies (int > 0,int > 0)
        self.type = type

        a = np.array(coeficents)
        b = [dim] * (type[0] + type[1])
        if a.shape != tuple(b):
            raise ValueError(
                "Coeficents array does not alighn with tensor type and dimension -- type: " + str(
                    type) + " dimension: " + str(dim) + " so the array needs to have dimensions:" + str(
                    b) + "and currently is " + str(a.shape))
        self.coeficents = coeficents

    # Name of tensor can be used for debuging and printing, is optional and if not inputed then will be set too "T": string
    def setName(self, a):
        self._name = a

    def getName(self):
        return getattr(self, "_name", "T")

    name = property(getName, setName)

    def showTensor(self):
        tensorString = ""

        # Adding Tensor name including indicies to the start of the print out
        headerName = self.getName()

        if self.type[0] != 0 or self.type[1] != 0:
            if self.type[1] == 0:
                tensorString += printIndicies(headerName, self.type[0], 0, True) + " =\n\n"
            if self.type[0] == 0:
                tensorString += printIndicies(headerName, self.type[1], 0, False) + " =\n\n"
            if self.type[0] != 0 and self.type[1] != 0:
                tensorString += printIndicies(printIndicies(headerName, self.type[0], 0, True), self.type[1],
                                              self.type[0], False) + " =\n\n"
        else:
            tensorString = headerName + " =\n\n"

        # Adding the coeficents to the print out with dynamic formatting
        if self.type[0] + self.type[1] == 0:
            tensorString += str(self.coeficents)

        if self.type[0] + self.type[1] == 1:
            if self.type[0] == 1:
                for i in range(self.dim):
                    tensorString += str(self.coeficents[i]) + "\n"
            else:
                for i in range(self.dim):
                    tensorString += str(self.coeficents[i]) + "  "

        if self.type[0] + self.type[1] == 2:
            tempPosSave = [[False]*self.dim]*self.dim
            length = [" "] * self.dim
            for i in range(self.dim):
                for j in range(self.dim):
                    if len(str(self.coeficents[i][j])) > len(length[i]):
                        length[j] = " "*(len(str(self.coeficents[i][j])))
                        print("test",i,j)
                        tempPosSave[i][j] = True

            posSave = list(np.array(tempPosSave))
            for i in range(self.dim):
                for j in range(self.dim):
                    if posSave[i][j] or j == self.dim-2:
                        tensorString += str(self.coeficents[i][j]) + " "
                    else:
                        tensorString += str(self.coeficents[i][j]) + length[j]
                tensorString += "\n"
        print(length)

        print(tensorString)


if __name__ == '__main__':
    a = [[1000000000000, 1, 1,1], [1, 1, 10000,1], [1, 1, 1,1],[1,1,1,1]]
    test = tensor(4, (1, 1, 1, 1), (1, 1), a)
    test.showTensor()
