import numpy as np
import string


def subTensorHeader(input, pos):
    letters = list(string.ascii_lowercase)
    for i in pos:
        input.replace(letters[i], str(i))
    return input


def permutationsRepeatitionsRecur(n, left, k):
    # Pushing this vector to a vector of vector
    if (k == 0):
        permutationsOutput.append(tempPermutationsOutput[:])
        return
    for i in range(left, n + 1):
        tempPermutationsOutput.append(i)
        permutationsRepeatitionsRecur(n, i + 1, k - 1)
        tempPermutationsOutput.pop()


def permutationsRepeatitions(dim,rank):
    permutationsRepeatitionsRecur(dim,1, rank)
    return permutationsOutput


def formatted2Darray(dim, coeficents, tensorString):
    posSave = [[False] * dim for _ in range(dim)]
    length = [" "] * dim
    for i in range(dim):
        for j in range(dim):
            if len(str(coeficents[i][j])) > 1:
                length[j] = " " * (len(str(coeficents[i][j])))
                posSave[i][j] = True

    for i in range(dim):
        for j in range(dim):
            if posSave[i][j]:
                tensorString += str(coeficents[i][j]) + " "
            else:
                tensorString += str(coeficents[i][j]) + length[j]
        tensorString += "\n"
    return tensorString


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
                    b) + "and currently is " + str(a.shape))
        self.coeficents = coeficents

    # Name of tensor can be used for debuging and printing, is optional and if not inputed then will be set too "T": string
    def setName(self, a):
        self._name = a

    def getName(self):
        return getattr(self, "_name", "T")

    name = property(getName, setName)

    def showTensor(self):
        global permutationsOutput
        global tempPermutationsOutput
        permutationsOutput = []
        tempPermutationsOutput = []
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
            #Broken indiceis of sub array print outs dont repeat look too permutationsRepitition()
            nonPresentableRank = self.type[0] + self.type[1] - 2
            permutationsRepeatitions(self.dim,nonPresentableRank)
            letters = list(string.ascii_lowercase)
            copyTensorString = [tensorString]*len(permutationsOutput)
            for i in range(len(permutationsOutput)):
                for j in range(len(permutationsOutput[i])):
                    copyTensorString[i] = copyTensorString[i].replace(letters[j],str(permutationsOutput[i][j]))
                    copyTensorString[i] += "hello \n\n"
                tensorString += copyTensorString[i]

        print(tensorString)


if __name__ == '__main__':
    a = np.zeros((3,3,3,3))
    test = tensor(3, (1, 1,1), (1, 3), a)
    test.showTensor()
