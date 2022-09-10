import string
import numpy as np
import itertools


def acsessSubArray(c, dim, rank, pos):
    a = dim ** (rank)
    reformatC = np.array(c).reshape((1, a))[0]
    index = 0
    for i in range(len(pos)):
        index += pos[i] * (dim ** (i + 2))
    outputC = reformatC[index:index + (dim ** 2)]
    return outputC.reshape((dim, dim))


def permutationsRepeatitions(n, k):
    x = [i for i in range(n)]
    output = [p for p in itertools.product(x, repeat=k)]
    return output


def formatted2Darray(dim, coeficents, tensorString):
    maxLengthColumn = [0]*dim
    for i in range(dim):
        for j in range(dim):
            if len(str(coeficents[j][i])) >= maxLengthColumn[i]:
                maxLengthColumn[i] = len(str(coeficents[j][i])) + 1
    for i in range(dim):
        for j in range(dim):
            tensorString += str(coeficents[i][j]) + " "*(maxLengthColumn[i]-len(str(coeficents[i][j])))
        tensorString += "\n"
    print(tensorString)


def printIndicies(a, n, m, state1):
    # if state1 is equal too True then we do contravariant and if False we do covariant
    # if state2 is equal to False for header tensor name and True for header tensor name of sub rank 2 tensors
    letters = list(string.ascii_lowercase)
    if state1:
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

        b = [dim] * (type[0] + type[1])
        if np.array(coeficents).shape != tuple(b):
            raise ValueError(
                "Coeficents array does not alighn with tensor type and dimension -- type: " + str(
                    type) + " dimension: " + str(dim) + " so the array needs to have dimensions:" + str(
                    b) + "and currently is " + str(np.array(coeficents).shape))
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
            tensorString = formatted2Darray(self.dim, self.coeficents, tensorString)

        if self.type[0] + self.type[1] > 2:
            #by fixing the formatted2DArray subroutine we broke the showtensor attribute function idk why
            nonPresentableRank = self.type[0] + self.type[1] - 2
            permutationsOutput = permutationsRepeatitions(self.dim, nonPresentableRank)
            letters = list(string.ascii_lowercase)
            copyTensorString = [tensorString] * len(permutationsOutput)
            for i in range(len(permutationsOutput)):
                for j in range(len(permutationsOutput[i])):
                    copyTensorString[i] = copyTensorString[i].replace(letters[j], str(permutationsOutput[i][j]))
                    copyTensorString[i] = formatted2Darray(self.dim, acsessSubArray(self.coeficents, self.dim,self.type[0] + self.type[1],permutationsOutput[i]),copyTensorString[i])
                tensorString += copyTensorString[i] + "\n"

        print(tensorString)


if __name__ == '__main__':
    a = np.random.randint(10000,size = (4,4))
    test = tensor(4, (1, 1, 1, 1), (0, 2), a)
    test.showTensor()
