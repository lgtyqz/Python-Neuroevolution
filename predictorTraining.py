from linearRegression import *
x = LinearRegression(Matrix([[1]]), Matrix([[1]]))
x.loadData("gen0Data.txt")
prevJ = 2 ** 32
currentJ = x.gradientDescent(0.1)
while prevJ - currentJ > 0.01:
    prevJ = copy.copy(currentJ)
    currentJ = x.gradientDescent(0.1)
x.writeData("linRegGen0Data.txt")
