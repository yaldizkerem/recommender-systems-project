import pandas as pd
from sklearn.decomposition import PCA
import numpy as np

data = pd.read_csv('u.data', sep='\t', names=['user', 'movie', 'rate', 'timestamp'])

dataSample = data.sample(frac=0.1)
dataSample = dataSample.loc[dataSample['rate'] == 5]
data.drop(dataSample.index, inplace=True)

data = data.pivot(index='user', columns='movie', values='rate').fillna(0)

userItem = PCA(n_components = 5).fit_transform(data)
itemUser = PCA(n_components = 5).fit_transform(data.T)

data.replace(to_replace=[3, 4, 5], value=1j, inplace=True)
data.replace(to_replace=[1, 2], value=-1j, inplace=True)

userUser = pd.DataFrame(data=userItem.T).corr()
itemItem = pd.DataFrame(data=itemUser.T).corr()

adjacencyMatrix = pd.concat([pd.DataFrame(data=userUser), pd.DataFrame(data=data.values)], axis=1)
adjacencyMatrix = pd.concat([adjacencyMatrix, pd.concat([pd.DataFrame(data=data.T.values).multiply(-1), pd.DataFrame(data=itemItem)], axis=1)])

tempMatrix = np.dot(adjacencyMatrix, adjacencyMatrix)

hitRates = [[],[],[],[],[],[],[],[],[],[]]
coverageRates = [[],[],[],[],[],[],[],[],[],[]]

for length in range(3):    
    adjacencyMatrix = np.dot(tempMatrix, adjacencyMatrix)
    resultMatrix = adjacencyMatrix[:len(userUser),len(userUser):]

    suggestions = {}
    for top in range(1, 11):
        suggestedMovie = []
        for index, row in enumerate(np.argsort(resultMatrix, axis=1)[:, :(-10 * top - 1):-1]):
            suggestions[data.index.values[index]] = data.columns[row].values
            suggestedMovie += list(data.columns[row].values)
        hit = miss = 0
        for item in dataSample[['user', 'movie']].values:
            try:
                if item[1] in suggestions[item[0]]: hit += 1
                else: miss += 1
            except:
                pass
        hitRates[top - 1].append(hit / (float(hit) + miss) * 100)
        coverageRates[top - 1].append(len(set(suggestedMovie))/float(len(itemItem)) * 100)

from gpcharts import figure

hitFigure = figure(title = 'Hits Rate Comparison', ylabel = 'Hits Rate')
xValues = ['Top-N']
yValues = [['Length=3', 'Length=5', 'Length=7']]

for index, hit in enumerate(hitRates):
    xValues += [(index + 1) * 10]
    yValues += [hit]

hitFigure.plot(xValues, yValues)

hitFigure = figure(title = 'Coverage Comparison', ylabel = 'Coverage')
yValues = [['Length=3', 'Length=5', 'Length=7']]

for coverage in coverageRates:
    yValues += [coverage]

hitFigure.plot(xValues, yValues)
