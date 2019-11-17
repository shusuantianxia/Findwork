import pandas as pd
import numpy as np
data1 = pd.read_csv('../wechat0/houseprice.csv')
data = np.array(data1).reshape(-1, 3)
c = len(data)
for i in range(c):
    data[i, 1] = data[i, 1] + '市'
data4 = np.concatenate((data[:, 0].reshape(-1, 1), data[:, 2].reshape(-1, 1)), axis=1)
data5 = data[:, 1:].reshape(-1, 2)
data6 = data4[np.lexsort(-data4.T)]
for i in range(c):
    for j in range(c):
        if float(data6[i, 1]) == float(data5[j, 1]):
            data6[i, 0] = data5[j, 0]
data7 = np.arange(1, c+1).reshape(-1, 1)
data6 = np.concatenate((data6, data7), axis=1)
print(data6)