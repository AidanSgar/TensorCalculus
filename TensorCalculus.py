import numpy as np
import string

def printIndicies(a,n,m,state):
    # if state is equal too True then we do contravariant and if False we do covariant
    letters = list(string.ascii_lowercase)
    if state:
        a += "^("
    else:
        a += "_("
    for i in range(m,n+m):
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
        if a.ndim != type[0] + type[1]:
            raise ValueError(
                "Rank of coeficents array does not alighn with tensor type -- type: " + str(type) + " rank: " + str(
                    a.ndim))
        self.coeficents = coeficents


    # Name of tensor can be used for debuging and printing, is optional and if not inputed then will be set too "T": string
    def setName(self, a):
        self._name = a

    def getName(self):
        return getattr(self, "_name", "T")

    name = property(getName, setName)

    def showTensor(self):
        tensorString = ""
        headerName = self.getName()

        if self.type[0] != 0 or self.type[1] != 0:
            if self.type[1] == 0:
                tensorString += printIndicies(headerName,self.type[0],0,True) + " =\n\n"
            if self.type[0] == 0:
                tensorString += printIndicies(headerName,self.type[1],0,False) + " =\n\n"
            if self.type[0] != 0 and self.type[1] != 0:
                tensorString += printIndicies(printIndicies(headerName,self.type[0],0,True),self.type[1],self.type[0],False) + " =\n\n"
        else:
            tensorString = headerName + " =\n\n"

        if self.type[0] + self.type[1] == 0:
            tensorString += str(self.coeficents)
        if self.type[0] + self.type[1] == 1:
            if self.type[0] == 1:
                for i in range(self.dim):
                    tensorString += str(self.coeficents[i]) + "\n"
            else:
                for i in range(self.dim):
                    tensorString += str(self.coeficents[i]) + "  "

        print(tensorString)




if __name__ == '__main__':
    a = tensor(3,(1,1,1),(0,1),[1,2,3])
    a.showTensor()