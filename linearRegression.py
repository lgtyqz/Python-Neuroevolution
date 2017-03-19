from matrix import *
class LinearRegression:
    def __init__(self, inputData, outputData):
        assert type(inputData) == Matrix, \
               "The input data must be in a matrix."
        assert type(outputData) == Matrix, \
               "The output data must also be in a matrix."
        self.inputData = inputData
        # Vertical Matrix/Column Vector
        self.outputData = outputData
        # Row List
        self.theta = []
        self.j = []
        for i in range(self.inputData.size[1]):
            self.theta.append(0)
    def gradientDescent(self, alpha, LAMBDA=0):
        hX = []
        sums = []
        # Cost function
        for i in self.inputData.matrixData:
##            print(len(i))
##            print(len(self.theta))
            hX.append(
                (Matrix([i]) * Matrix(Matrix([self.theta]).transpose()))[0])
        hX = Matrix(hX)
        sums = Matrix(hX - self.outputData)
##        print("SUMS:", sums.matrixData)
        J = 1/(2 * len(self.inputData.matrixData)) * \
              Matrix(sums.POW(2)).sum()
        print("J =", J)
        for i in range(len(self.theta)):
            LIST = []
            for j in self.inputData.matrixData:
                LIST.append([j[i]])
##            print(LIST)
            LIST = Matrix(LIST)
            SUM = Matrix(sums.elemTimes(LIST)).sum()
##            print(SUM)
            self.theta[i] = self.theta[i] - alpha * \
                            (1/len(self.outputData.matrixData)) * SUM
            # Regularization is a W.I.P.
##        print(self.theta)
        return J
    def writeData(self, filename):
        print("File writing in progress...")
        file = open(filename, "w")
        for i in range(len(self.inputData.matrixData)):
            for j in self.inputData.matrixData[i]:
                file.write(str(j) + " ")
            file.write("\n")
            file.write(str(self.outputData.matrixData[i][0]) + "\n")
        file.write("THETA\n")
        for i in self.theta:
            file.write(str(i) + " ")
        file.close()
        print("File writing complete.")
    def loadData(self, filename):
        print("File loading in progress...")
        file = open(filename, "r")
        self.inputData = []
        self.outputData = []
        THETALINE = False
        for (count, line) in enumerate(file):
            contents = line.rstrip().split(" ")
##            print("Len:", len(contents))
            if not THETALINE:
                if line != "THETA\n":
                    if count % 2 == 0:
                        inputRow = []
                        for i in contents:
                            inputRow.append(float(i))
                        self.inputData.append(inputRow)
                    else:
                        self.outputData.append([float(contents[0])])
                else:
                    THETALINE = True
                    self.theta = []
            else:
                for i in contents:
                    self.theta.append(float(i))

        self.inputData = Matrix(self.inputData)
        self.outputData = Matrix(self.outputData)
        if not THETALINE:
            self.theta = []
            for i in range(self.inputData.size[1]):
                self.theta.append(0)
            print(len(self.theta))
            print(self.inputData.size[1])
        file.close()
        print("File loading complete.")
    def prediction(self, inputData):
        assert type(inputData) == list, "Input data must be in a list."
        data = Matrix([inputData])
        return (data * Matrix(Matrix([self.theta]).transpose()))[0][0]
