import numpy as np

#X = np.array([ [0,0,1],[0,1,1],[1,0,1],[1,1,1] ])
#y = np.array([[0,1,1,0]]).T
#syn0 = 2*np.random.random((3,4)) - 1
#syn1 = 2*np.random.random((4,1)) - 1
#for j in range(60000):
#    l1 = 1/(1+np.exp(-(np.dot(X,syn0))))
#    l2 = 1/(1+np.exp(-(np.dot(l1,syn1))))
#    l2_delta = (y - l2)*(l2*(1-l2))
#    l1_delta = l2_delta.dot(syn1.T) * (l1 * (1-l1))
#    syn1 += l1.T.dot(l2_delta)
#    syn0 += X.T.dot(l1_delta)
#    
#print(syn0)
#print(syn1)



#def nonlin(x, deriv = False):
#    if(deriv == True):
#        return f(x)*(1-f(x))
#    return 1/(1+np.exp(-x))
#
#X = np.array([
#    [0, 0, 1],
#    [0, 1, 1],
#    [1, 0, 1],
#    [1, 1, 1]
#])
#
#y = np.array([[0, 0, 1, 1]]).T
#
#np.random.seed(1)
#syn0 = 2*np.random.random((3, 1)) - 1
#
#for item in range(10000):
#    l0 = X
#    l1 = nonlin(np.dot(l0, syn0))
#    l1_error = y - l1
#    
#    l1_delta = l1_error * nonlin(l1, True)
#    
#    syn0 += np.dot(l0.T, l1_delta)
#    
#print('Выходные данные после тренировки: ')
#print(l1)
