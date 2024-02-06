import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv("data\\data_train.csv")
data = np.array(data)
m, n = data.shape
np.random.shuffle(data) # shuffle before splitting into dev and training sets

data_dev = data[0:1000].T
Y_dev = data_dev[0]
X_dev = data_dev[0:n]

data_train = data[1000:m].T
Y_train = data_train[0]
X_train = data_train[0:n]
_,m_train = X_train.shape

print(X_train)

def init_params():
    W1 = np.random.normal(size=(15, 15)) * np.sqrt(1./15)
    b1 = np.random.normal(size=(15, 1)) * np.sqrt(1/15)
    W2 = np.random.normal(size=(15, 15)) * np.sqrt(1./30)
    b2 = np.random.normal(size=(15, 1)) * np.sqrt(1./15)
    #print(W1, b1, W2, b2)
    return W1, b1, W2, b2



def ReLU(Z):
    return np.maximum(Z, 0)

def softmax(Z):
    if isinstance(Z, (int, float)):
        exp_Z = np.exp(Z)
        return exp_Z / np.sum(exp_Z)
    else:
        exp_Z = np.exp(Z - np.max(Z))
        return exp_Z / np.sum(exp_Z, axis=0, keepdims=True)



    
def forward_prop(W1, b1, W2, b2, X):
    Z1 = W1.dot(X) + b1
   # print(Z1)
    A1 = ReLU(Z1)
    Z2 = W2.dot(A1) + b2
    A2 = softmax(Z2)

    return Z1, A1, Z2, A2


def ReLU_deriv(Z):
    return Z > 0

# def one_hot(Y):
#     max_value = int(np.nanmax(Y)) + 1 if not np.isnan(np.nanmax(Y)) else 0
#     one_hot_Y = np.zeros((Y.size, max_value))


    
#     return one_hot_Y


def backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y):
    
    dZ2 = A2
    dW2 = 1 / m * dZ2.dot(A1.T)
    db2 = 1 / m * np.sum(dZ2)
    dZ1 = W2.T.dot(dZ2) * ReLU_deriv(Z1)
    dW1 = 1 / m * dZ1.dot(X.T)
    db1 = 1 / m * np.sum(dZ1)
    return dW1, db1, dW2, db2

def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1    
    W2 = W2 - alpha * dW2  
    b2 = b2 - alpha * db2    
    return W1, b1, W2, b2

def get_predictions(A2):
    return A2

def get_accuracy(predictions, Y):

    return np.sum(predictions == Y) / Y.size

def gradient_descent(X, Y, alpha, iterations):
    W1, b1, W2, b2 = init_params()
    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
        dW1, db1, dW2, db2 = backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y)
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)
        if i % 10 == 0:

            predictions = get_predictions(A2)

            
    return W1, b1, W2, b2

W1, b1, W2, b2 = gradient_descent(X_train, Y_train, 0.10, 10)



def make_predictions(X, W1, b1, W2, b2):
    _, _, _, A2 = forward_prop(W1, b1, W2, b2, X)
    predictions = get_predictions(A2)
    return predictions

def test_prediction(index, W1, b1, W2, b2):
    prediction = make_predictions(X_train[:, index, None], W1, b1, W2, b2)
    print(prediction)
    
   

test_prediction(0, W1, b1, W2, b2)

# import os

# def generate_salt():
#     return os.urandom(16)

# def custom_hash(data):
#     # Simple custom hash function using XOR bitwise operations
#     result = 0
#     for char in data:
#         result ^= ord(char)
#     print(result)
#     return result

# def hash_password(password, salt=None):
#     if salt is None:
#         salt = generate_salt()

#     # Combine password and salt, and hash using custom_hash function
#     hashed_password = custom_hash(password + str(salt, 'latin-1'))

#     # Return salt and hashed password
#     return salt, hashed_password

# def verify_password(password, stored_salt, stored_hashed_password):
#     # Combine password and stored salt, and hash using custom_hash function
#     hashed_password = custom_hash(password + str(stored_salt, 'latin-1'))

#     # Compare the hashed password with the stored hashed password
#     return hashed_password == stored_hashed_password

# # Example usage:
# password_to_hash = "secure_password"
# salt, hashed_password = hash_password(password_to_hash)

# # Store salt and hashed password in a database
# # ...

# # Verify a password
# entered_password = "secure_password"
# if verify_password(entered_password, salt, hashed_password):
#     print("Password is correct!")
# else:
#     print("Incorrect password.")