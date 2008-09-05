__author__ = 'Tom Schaul, tom@idsia.ch'

from scipy import array, exp, tanh, clip, log, dot, sqrt, power, pi, tan, diag, rand
from scipy.linalg import inv, det, svd


def semilinear(x):
    """ This function ensures that the values of the array are always positive. It is 
        x+1 for x=>0 and exp(x) for x<0. """
    try:
        # assume x is a numpy array
        shape = x.shape
        x.flatten()
        x = x.tolist()
    except AttributeError:
        # no, it wasn't: build shape from length of list
        shape = (1, len(x))
    def f(val):
        if val<0:
            # exponential function for x<0
            return safeExp(val)
        else:
            # linear function for x>=0
            return val+1.0
    return array(map(f, x)).reshape(shape)


def semilinearPrime(x):
    """ This function is the first derivative of the semilinear function (above).
        It is needed for the backward pass of the module. """
    try:
        # assume x is a numpy array
        shape = x.shape
        x.flatten()
        x = x.tolist()
    except AttributeError:
        # no, it wasn't: build shape from length of list
        shape = (1, len(x))
    def f(val):
        if val<0:
            # exponential function for x<0
            return safeExp(val)
        else:
            # linear function for x>=0
            return 1.0
    return array(map(f, x)).reshape(shape)


def safeExp(x):
    """ bounded range for the exponential function """         
    return exp(clip(x, -500, 500))


def sigmoid(x):
    return 1./(1.+safeExp(-x))


def sigmoidPrime(x):
    tmp = sigmoid(x)
    return tmp*(1-tmp)


def tanhPrime(x):
    tmp = tanh(x)
    return 1-tmp*tmp
    
            
def ranking(R):
    """ produce a linear ranking of the values in R """        
    l = sorted(list(enumerate(R)), cmp = lambda a,b: cmp(a[1],b[1]))
    l = sorted(list(enumerate(l)), cmp = lambda a,b: cmp(a[1],b[1]))
    return array(map(lambda (r, dummy): r, l))


def expln(x):
    """ This function ensures that the values of the array are always positive. It is 
        ln(x+1)+1 for x=>0 and exp(x) for x<0. """
    def f(val):
        if val<0:
            # exponential function for x<0
            return exp(val)
        else:
            # natural log function (slightly shifted) for x>=0
            return log(val+1.0)+1
    return array(map(f, x))


def explnPrime(x):
    """ This function is the first derivative of the self.expln function (above).
        It is needed for the backward pass of the module. """
    def f(val):
        if val<0:
            # exponential function for x<0
            return exp(val)
        else:
            # linear function for x>=0
            return 1.0/(val+1.0)
    return array(map(f, x))


def multivariateNormalPdf(z, x, sigma):
    assert len(z.shape) == 1 and len(x.shape) == 1 and len(x) == len(z) and sigma.shape == (len(x), len(z))
    tmp = -0.5 * dot(dot((z-x), inv(sigma)), (z-x))
    res = (1./power(2.0*pi, len(z)/2.)) * (1./sqrt(det(sigma))) * exp(tmp)
    return res   


def multivariateCauchy(mu, sigma, onlyDiagonal = True):
    if not onlyDiagonal:
        u, s, d = svd(sigma)
        coeffs = sqrt(s)
    else:
        coeffs = diag(sigma)
    r = rand(len(mu))
    res = coeffs*tan(pi*(r-0.5))
    if not onlyDiagonal:
        res = dot(d, dot(res, u))
    return res+mu 

