import numpy as np
import pandas as pd

#gets the data from the csv file
data = pd.read_csv("data\\data_train.csv")
data = np.array(data)
m, n = data.shape
np.random.shuffle(data) # shuffle before splitting into dev and training sets


#shapes all of the data so it can be operated on
data_train = data[1000:m].T
Y_train = data_train[0]
X_train = data_train[0:n]
_,m_train = X_train.shape


#initialises the weights and biases using Xavier Initialisation
def init_params():
    W1 = np.random.normal(size=(15, 15)) * np.sqrt(1./15)
    b1 = np.random.normal(size=(15, 1)) * np.sqrt(1/15)
    W2 = np.random.normal(size=(15, 15)) * np.sqrt(1./30)
    b2 = np.random.normal(size=(15, 1)) * np.sqrt(1./15)
    print(W1, b1, W2, b2)
    return W1, b1, W2, b2


#relu function
def ReLU(Z):
    return np.maximum(Z, 0)

def ReLU_deriv(Z):
    return Z > 0

#softmax function
def softmax(Z):
    if isinstance(Z, (int, float)):
        exp_Z = np.exp(Z)
        return exp_Z / np.sum(exp_Z)
    else:
        exp_Z = np.exp(Z - np.max(Z))
        return exp_Z / np.sum(exp_Z, axis=0, keepdims=True)


#forward propagation 
def forward_prop(W1, b1, W2, b2, X):
    Z1 = W1.dot(X) + b1
    A1 = ReLU(Z1)
    Z2 = W2.dot(A1) + b2
    A2 = softmax(Z2)
    return Z1, A1, Z2, A2


#backwards propagation
def backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y):
    
    dZ2 = A2
    dW2 = 1 / m * dZ2.dot(A1.T)
    db2 = 1 / m * np.sum(dZ2)
    dZ1 = W2.T.dot(dZ2) * ReLU_deriv(Z1)
    dW1 = 1 / m * dZ1.dot(X.T)
    db1 = 1 / m * np.sum(dZ1)
    return dW1, db1, dW2, db2

#updates the paramaters of the weights and biases so that they can be used with higher accuracy
def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1    
    W2 = W2 - alpha * dW2  
    b2 = b2 - alpha * db2    
    return W1, b1, W2, b2


#calls all the functions for the training process
def gradient_descent(X, Y, alpha, iterations):
    W1, b1, W2, b2 = init_params()
    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
        dW1, db1, dW2, db2 = backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y)
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)     
    return W1, b1, W2, b2


#gets the final weights and biases to be used in the final product
W1, b1, W2, b2 = gradient_descent(X_train, Y_train, 0.10, 10)



