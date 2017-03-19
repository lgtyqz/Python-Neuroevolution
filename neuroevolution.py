from neuralNetwork import *
class NNPopulation:
    def __init__(self, numOrganisms, deathRate, numInputUnits, numOutputUnits,
                 numHiddenLayers, numHidUnits, mutationRate, genesMutProb,
                 weightLimit):
        self.listOfNames = []
        names = open("names.txt", "r")
        speciesNames = []
        surnames = open("surnames.txt", "r")
        for i in names:
            self.listOfNames.append(i.rstrip())
        for i in surnames:
            speciesNames.append(i.rstrip())
        names.close()
        surnames.close()
        self.usedNames = copy.deepcopy(self.listOfNames)
        self.organisms = []
        self.numInputUnits = numInputUnits
        self.numOutputUnits = numOutputUnits
        self.numHiddenLayers = numHiddenLayers
        self.numHidUnits = numHidUnits
        self.mutationRate = mutationRate
        self.genesMutProb = genesMutProb
        self.generation = 0
        for i in range(numOrganisms):
            if len(self.usedNames) == 0:
                self.usedNames = copy.deepcopy(self.listOfNames)
            index = random.randint(0, len(self.usedNames) - 1)
            name = self.usedNames[index]
            del self.usedNames[index]
            print(name)
            self.organisms.append([Neural_Network(numInputUnits, numOutputUnits,
                                                 numHiddenLayers, numHidUnits,
                                                  None, weightLimit, name),
                                   0])
        # The number of organisms that die
        self.deathRate = deathRate
        self.weightLimit = weightLimit
    def nextGeneration(self):
        # Step 1: Rank and order by points
        self.organisms = sorted(self.organisms, key=lambda org:org[1])
        # Step 2: KILL THE WEAK
        del self.organisms[:self.deathRate]
        # Step 3: Have the remainder of the organisms make babies.
        children = []
        for i in range(len(self.organisms)):
            # Reset points
            # print("Self:", self.organisms[i][0].weights[0].matrixData)
            self.organisms[i][1] = 0
            if i != len(self.organisms) - 1:
                mate = self.organisms[i + 1]
            else:
                mate = self.organisms[i - 1]
            # print("Mate:", mate.weights[0].matrixData)
            childWeights = []
            # Combine "Genes"
## Old method: Average of weights
## Dr. Miller's student's method: Randomly choose weight
## New method (WIP): If they're the same, take the average. Otherwise, choose
            ## the guy with the highest fitness.
            for layer in range(len(self.organisms[i][0].weights)):
                childWeightMatrix = []
                for node in range(len(
                    self.organisms[i][0].weights[layer].matrixData)):
                    childNodeWeights = []
                    for weight in range(len(
                        self.organisms[i][0].weights[layer].matrixData[node])):
                        rand = (random.random() <= 0.5)
                        possibleWeights = [
                            self.organisms[i][0].weights[layer].matrixData[node][weight],
                            mate[0].weights[layer].matrixData[node][weight]]
                        if int(possibleWeights[0] > 0) == int(possibleWeights[1] > 0) \
                           and abs(possibleWeights[0] - possibleWeights[1] < 4):
                            childNodeWeights.append(round((
                                possibleWeights[0] + possibleWeights[1])/2, 2))
                        else:
                            if self.organisms[i][1] > mate[1]:
                                childNodeWeights.append(possibleWeights[0])
                            elif self.organisms[i][1] < mate[1]:
                                childNodeWeights.append(possibleWeights[1])
                            else:
                                childNodeWeights.append(possibleWeights[random.randint(0, 1)])
                    childWeightMatrix.append(childNodeWeights)
                childWeightMatrix = Matrix(childWeightMatrix)
                childWeights.append(childWeightMatrix)
            if len(self.usedNames) == 0:
                self.usedNames = copy.deepcopy(self.listOfNames)
            index = random.randint(0, len(self.usedNames) - 1)
            name = self.usedNames[index]
            del self.usedNames[index]
##            self.organisms.append([Neural_Network(numInputUnits, numOutputUnits,
##                                                 numHiddenLayers, numHidUnits,
##                                                  None, weightLimit, name),
##                                   0])

            # print("Child:", childWeights[0].matrixData)
            children.append([Neural_Network(self.numInputUnits,
                                                 self.numOutputUnits,
                                                 self.numHiddenLayers,
                                                 self.numHidUnits,
                                                  childWeights,
                                            self.weightLimit, name), 0])

        for i in children:
            self.organisms.append(i)
        # Step 4: MUTATE!!!
        for i in range(len(self.organisms)):
            random.seed()
            if random.random() < self.mutationRate:
                for layer in range(len(self.organisms[i][0].weights)):
                    for node in range(len(
                        self.organisms[i][0].weights[layer].matrixData)):
                        for weight in range(len(
                        self.organisms[i][0].weights[layer].matrixData[node])):
                            random.seed()
                            if random.random() < self.genesMutProb:
                                print("Mutation!")
                                print("Old value:", self.organisms[i][0].weights[layer].matrixData[node][weight])
                                mutateValue = random.randint(
                                    -self.weightLimit,
                                    self.weightLimit)
                                print("New value:", mutateValue)
                                self.organisms[i][0].weights[layer].matrixData[node][weight] = mutateValue

            
        self.generation += 1
                    
    def writeGeneration(self, filename):
        file = open(filename, "w")
        # File format:
        #
        # First line: Death rate, mutationRate, genesmutprob, weightLimit
        # These are all population parameters.
        #
        # Second line: numInputUnits, numOutputUnits, numHiddenLayers,
        # numHidUnits
        # These are all neural network parameters.
        file.write(str(self.generation) + "\n")
        file.write("{0} {1} {2} {3}\n".format(self.deathRate, self.mutationRate,
                                        self.genesMutProb, self.weightLimit))
        file.write("{0} {1} {2} {3}\n".format(self.numInputUnits,
                                              self.numOutputUnits,
                                              self.numHiddenLayers,
                                              self.numHidUnits))
        # Next up: The weights, all confined to a single line.
        print("\nFile writing in progress...")
        count = 0
        for i in self.organisms:
            weightString = ""
            for j in i[0].weights:
                for node in j.matrixData:
                    for weight in node:
                        weightString += "{0} ".format(str(weight))

            weightString += "\n"
            file.write(weightString)
            count = count + 1
        print(count)
        file.close()
        print("File writing complete.\n")
    def loadGeneration(self, filename):
        print("\nFile loading...")
        self.organisms = []
        file = open(filename, "r")
        for (count, l) in enumerate(file):
            line = l.rstrip()
            pieces = line.split(" ")
            if count == 0:
                self.generation = int(pieces[0])
            elif count == 1:
                self.deathRate = int(pieces[0])
                self.mutationRate = float(pieces[1])
                self.genesMutProb = float(pieces[2])
                self.weightLimit = int(pieces[3])
            elif count == 2:
                self.numInputUnits = int(pieces[0])
                self.numOutputUnits = int(pieces[1])
                self.numHiddenLayers = int(pieces[2])
                self.numHidUnits = int(pieces[3])
            else:
                weights = []
                layer0Weights = []
                counter = 0
                # Adapting the neural network random weight generation alg here
                for i in range(self.numInputUnits + 1):
                    nodeWeights = []
                    if self.numHiddenLayers > 0:
                        for j in range(self.numHidUnits):
                            nodeWeights.append(float(pieces[counter]))
                            counter += 1
                    else:
                        for j in range(self.numOutputUnits):
                            nodeWeights.append(float(pieces[counter]))
                            counter += 1
                    layer0Weights.append(nodeWeights)
                layer0Weights = Matrix(layer0Weights)
                weights.append(layer0Weights)
                if self.numHiddenLayers > 0:
                    for layer in range(self.numHiddenLayers):
                        hidLayerWeights = []
                        for i in range(self.numHidUnits + 1):
                            nodeWeights = []
                            if layer == self.numHiddenLayers - 1:
                                for j in range(self.numOutputUnits):
                                    nodeWeights.append(float(pieces[counter]))
                                    counter += 1
                            else:
                                for i in range(self.numHidUnits):
                                    nodeWeights.append(float(pieces[counter]))
                                    counter += 1

                            hidLayerWeights.append(nodeWeights)
                        hidLayerWeights = Matrix(hidLayerWeights)
                        weights.append(hidLayerWeights)
                if len(self.usedNames) == 0:
                    self.usedNames = copy.deepcopy(self.listOfNames)
##                name = self.usedNames[random.randint(0, len(self.usedNames) - 1)]
##                self.organisms.append([Neural_Network(self.numInputUnits, self.numOutputUnits,
##                                                     self.numHiddenLayers, self.numHidUnits,
##                                                      None, self.weightLimit, name),
##                                       0])

                newOrganism = [Neural_Network(self.numInputUnits,
                                              self.numOutputUnits,
                                              self.numHiddenLayers,
                                              self.numHidUnits, weights), 0]
                self.organisms.append(newOrganism)

        file.close()
        print("File reading complete.\n")
        
                                                 
