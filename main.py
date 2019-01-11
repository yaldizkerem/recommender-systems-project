import pandas as pd
from sklearn.decomposition import PCA
import numpy as np

data = pd.read_csv('u.data', sep='\t', names=['user', 'movie', 'rate', 'timestamp'])

dataSample = data.sample(frac=0.1)
dataFiveStars = dataSample.loc[dataSample['rate'] != 5]
data.drop(dataSample.index, inplace=True)
data = data.append(dataFiveStars)
dataSample.drop(dataFiveStars.index, inplace=True)

data = data.pivot(index='user', columns='movie', values='rate')

dataFilled = data.fillna(0)
data.fillna(0, inplace=True)

userItem = PCA(n_components = 5).fit_transform(dataFilled)
itemUser = PCA(n_components = 5).fit_transform(dataFilled.T)

data.replace(to_replace=[3, 4, 5], value=1j, inplace=True)
data.replace(to_replace=[1, 2], value=-1j, inplace=True)

userUser = pd.DataFrame(data=userItem.T).corr()
itemItem = pd.DataFrame(data=itemUser.T).corr()

adjacencyMatrix = pd.concat([pd.DataFrame(data=userUser), pd.DataFrame(data=data.values)], axis=1)
adjacencyMatrix = pd.concat([adjacencyMatrix, pd.concat([pd.DataFrame(data=data.T.values), pd.DataFrame(data=itemItem)], axis=1)])

adjacencyMatrix = np.dot(np.dot(adjacencyMatrix, adjacencyMatrix), adjacencyMatrix)
resultMatrix = adjacencyMatrix[:len(userUser),len(userUser):]

suggestions = {}

for index, row in enumerate(np.argsort(resultMatrix, axis=1)[:, :-11:-1]):
    suggestions[data.index.values[index]] = data.columns[row].values
hit = miss = 0
for item in dataSample[['user', 'movie']].values:
    try:
        if item[1] in suggestions[item[0]]:
            hit+=1
        else:
            miss+=1
    except:
        pass
print("miss: " + str(miss))
print("hit: " + str(hit))
print("hit rate: " + str(hit/(float(hit)+miss)*100))
