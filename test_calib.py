import numpy as np

class KalmanFilter:
    def __init__(self, A, H, Q, R, x0, P0):
        self.A = A
        self.H = H
        self.Q = Q
        self.R = R
        self.x = x0
        self.P = P0
    
    def predict(self, u=0):
        self.x = np.dot(self.A, self.x) + u
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
    
    def update(self, z):
        y = z - np.dot(self.H, self.x)
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        self.x = self.x + np.dot(K, y)
        self.P = np.dot(np.eye(len(self.x)) - np.dot(K, self.H), self.P)
        
def kalman_filter(y):
    dt = 0.01
    A = np.array([[1, dt], [0, 1]])
    H = np.array([[1, 0], [0, 1]])
    Q = np.array([[0.1, 0], [0, 0.1]])
    R = np.array([[1, 0], [0, 1]])
    x0 = np.array([y[0], 0])
    P0 = np.eye(2) * 0.1
    
    kf = KalmanFilter(A, H, Q, R, x0, P0)
    
    filtered_y = np.zeros_like(y)
    
    for i in range(len(y)):
        kf.predict()
        kf.update(np.array([y[i], 0]))
        filtered_y[i] = kf.x[0]
    
    return filtered_y


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    t = np.arange(0, 10, 0.01)
    y = 5 * np.sin(t)
    y_noisy = y + np.random.normal(0, 1, len(t))
    print("======================== y_noisy ========================")
    print(y_noisy)
    

    
    plt.plot(t, y, label="signal")
    plt.plot(t, y_noisy, label="signal bruité")
    plt.plot(t, kalman_filter(y_noisy), label="signal filtré")
    plt.legend()
    plt.show()