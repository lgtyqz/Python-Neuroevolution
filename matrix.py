import math
import copy
class Matrix:
    def __init__(self, matrixData):
        assert type(matrixData) == list and type(matrixData[0]) == list, \
        "Invalid input. Matrix must be a two-dimensional list."
        self.matrixData = matrixData
        # Rows, Columns
        self.size = [len(matrixData), len(matrixData[0])]
    def __add__(self, other):
        if type(other) == Matrix:
            if self.size == other.size:
                returnMatrix = []
                for i in range(self.size[0]):
                    returnRow = []
                    for j in range(self.size[1]):
                        returnRow.append(self.matrixData[i][j] + \
                                         other.matrixData[i][j])
                    returnMatrix.append(returnRow)
                return returnMatrix
            else:
                raise ArithmeticError("Matrix dimensions do not match.")
        elif type(other) == float or type(other) == int:
            returnMatrix = []
            for i in range(self.size[0]):
                returnRow = []
                for j in range(self.size[1]):
                    returnRow.append(self.matrixData[i][j] + other)
                returnMatrix.append(returnRow)
            return returnMatrix
        else:
            raise TypeError("You can't add a matrix and that type.")
    def __sub__(self, other):
        if type(other) == Matrix:
            if self.size == other.size:
                returnMatrix = []
                for i in range(self.size[0]):
                    returnRow = []
                    for j in range(self.size[1]):
                        returnRow.append(self.matrixData[i][j] - \
                                         other.matrixData[i][j])
                    returnMatrix.append(returnRow)
                return returnMatrix
            else:
                raise ArithmeticError("Matrix dimensions do not match.")
        elif type(other) == float or type(other) == int:
            returnMatrix = []
            for i in range(self.size[0]):
                returnRow = []
                for j in range(self.size[1]):
                    returnRow.append(self.matrixData[i][j] - other)
                returnMatrix.append(returnRow)
            return returnMatrix
        else:
            raise TypeError("You can't subtract a matrix and that type.")
    def __mul__(self, other):
        if type(other) == Matrix:
            if self.size[1] == other.size[0]:
                returnMatrix = []
                for i in range(self.size[0]):
                    returnRow = []
                    for i2 in range(other.size[1]):
                        SUM = 0
                        for j in range(self.size[1]):
                            #print(other.matrixData[j][i2])
                            SUM += self.matrixData[i][j] * \
                                   other.matrixData[j][i2]
                        returnRow.append(SUM)
                    returnMatrix.append(returnRow)
                return returnMatrix
            else:
                raise ArithmeticError('''
    Matrix dimensions are not suitable for multiplication.''')
        elif type(other) == float or type(other) == int:
            returnMatrix = []
            for i in range(self.size[0]):
                returnRow = []
                for j in range(self.size[1]):
                    returnRow.append(self.matrixData[i][j] * other)
                returnMatrix.append(returnRow)
            return returnMatrix
        else:
            raise TypeError("You can't subtract a matrix and that type.")
    def __neg__(self):
        returnMatrix = []
        for i in range(self.size[0]):
            returnRow = []
            for j in range(self.size[1]):
                returnRow.append(-self.matrixData[i][j])
            returnMatrix.append(returnRow)
        return returnMatrix
    def sigmoid(self):
        returnMatrix = copy.deepcopy(self.matrixData)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                returnMatrix[i][j] = 1/(1 + math.e ** -self.matrixData[i][j])
                
        return returnMatrix
    def transpose(self):
        returnMatrix = []
        for j in range(self.size[1]):
            returnRow = []
            for i in range(self.size[0]):
                returnRow.append(self.matrixData[i][j])
            returnMatrix.append(returnRow)
        return returnMatrix
    def elemTimes(self, other):
        # Element-wise multiplication.
        assert type(other) == Matrix, \
               "The thing you're trying to multiply must also be a matrix."
        if self.size == other.size:
            returnMatrix = []
            for i in range(self.size[0]):
                returnRow = []
                for j in range(self.size[1]):
                    returnRow.append(self.matrixData[i][j] * \
                                     other.matrixData[i][j])
                returnMatrix.append(returnRow)
            return returnMatrix
        else:
            raise ArithmeticError("Matrix dimensions do not match.")
    def sum(self):
        SUM = 0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                SUM += self.matrixData[i][j]
        return SUM
    def POW(self, power):
        # Element-wise exponentation
        returnMatrix = copy.deepcopy(self.matrixData)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                returnMatrix[i][j] = self.matrixData[i][j] ** power
                
        return returnMatrix
        
    
