class tensor:
    def __init__(self,dim,sig,type):
        #Dimensionality of the manifold : int > 0
        self.dim = dim

        #Signature of the manifold: tuple (int,int)
        if len(sig) != dim:
            raise ValueError("Signature must be sasme length as the dimensionality -- dim: " + str(dim) + "  length of signature: "+str(len(sig)))
        self.sig = sig

        #Number of tensor product copies of tangent and cotangent space: tuple type[0] = tangent and type[1] = cotangent (int > 0,int > 0)
        self.type = type

    #Name of tensor can be used for debuging and is optional: string
    def setName(self,a):
        self._name = a
    def getName(self):
        return getattr(self,"_name","no name is given")
    name = property(getName,setName)



if __name__ == '__main__':
    test = tensor(2,(1,1),(0,1))
    print(test.dim, test.sig, test.type,"\n")
    test.name = "john"
    print(test.name)



