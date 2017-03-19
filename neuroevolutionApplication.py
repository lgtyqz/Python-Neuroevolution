# Imports.
from tkinter import *
from neuroevolution import *
from linearRegression import *
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
from statistics import *
import math
# Program parameters. I would put these as command line arguments, but I never
# use it, instead using IDLE.
askWhereTheFileGoes = False
recordGen0 = True
quitGen0 = False
CONTINUE = False
drawing = True
prediction = False
switchStage = False
playerInput = False
# Useful program variables.
gravity = 1
# The population object, used for storing, breeding, killing, and mutating
# organisms.
population = NNPopulation(30, 15, 206, 3, 2, 30, 0.1, 0.002, 8)
# This is a scrapped attempt at predicting the average score of generation 0
# for a given map. Unfortunately, there probably isn't any linear relationship.
soothsayer = LinearRegression(Matrix([[1]]), Matrix([[1]]))
soothsayer.loadData("linRegGen0Data.txt")
tiles = []
nnTiles = []
linRegTiles = []
timer = 0
timeLimit = 500
score = 0
minDist = 0
goalX = 0
goalY = 0
startX = 0
moveLeft = False
moveRight = False
class tile:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
    def draw(self):
        if self.t == 1:
            disp.create_rectangle(self.x, self.y, self.x + 40, self.y + 40,
                                  fill="black", outline="")
        elif self.t == 2:
            disp.create_rectangle(self.x, self.y, self.x + 40, self.y + 40,
                                  fill="red", outline="")
        elif self.t == 3:
            disp.create_oval(self.x, self.y, self.x + 40, self.y + 40,
                                fill="#FAC800", outline="")

class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
        self.jumping = False
        self.dead = False
        self.finished = False
    def moveRight(self, event=None):
        self.xVel += 0.5
    def moveLeft(self, event=None):
        self.xVel -= 0.5
    def jump(self, event=None):
        if not self.jumping:
            self.yVel = -18
            self.jumping = True
    def update(self):
        self.x += self.xVel
        self.y += self.yVel
        self.yVel += gravity
        self.xVel *= 0.9
        self.yVel *= 0.9
        for i in tiles:
            if i.t == 1:
                # Top collision, regain jump
                if self.x + 20 > i.x and \
                   self.x < i.x + 40 and \
                   self.y + 20 > i.y and \
                   self.y < i.y - 11:
                    self.y = i.y - 21
                    self.yVel *= -0.5
                    self.jumping = False
                    # print("TOP COLLISION")
                else:
                    # Left wall collision
                    if (self.x + 20 > i.x and \
                       self.x < i.x - 15) and \
                       self.y + 20 > i.y and \
                       self.y < i.y + 40:
                        self.xVel *= 0.5
                        self.x = i.x - 21
                        # print("LEFT WALL COLLISION")
                    # Right wall collision
                    if (self.x < i.x + 40 and \
                       self.x + 20 > i.x + 55) and \
                       self.y + 20 > i.y and \
                       self.y < i.y + 40:
                        self.xVel *= -0.5
                        self.x = i.x + 41
                        # print("RIGHT WALL COLLISION")
                    # Ceiling collision
                    if self.x + 20 > i.x and \
                       self.x < i.x + 40 and \
                       self.y < i.y + 40 and \
                       self.y + 20 > i.y:
                        self.yVel *= -0.5
                        self.y = i.y + 41
                        # print("CEILING COLLISION")
            if i.t == 2:
                if self.x + 20 > i.x and \
                   self.x < i.x + 40 and \
                   self.y + 20 > i.y and \
                   self.y < i.y + 40:
                    self.dead = True
            if i.t == 3:
                if self.x + 20 > i.x and \
                   self.x < i.x + 40 and \
                   self.y + 20 > i.y and \
                   self.y < i.y + 40:
                    self.finished = True
        if drawing:
            disp.create_rectangle(self.x, self.y, self.x + 20, self.y + 20,
                              fill="blue", outline="")
def populateTiles():
    global linRegTiles
    global nnTiles
    global tiles
    global goalX
    global goalY
    global startY
    nnTiles = []
    tiles = []
    linRegTiles = []
    madeAFinish = False
    startY = random.randint(0, 7)
    for x in range(0, 800, 40):
        nnTilesRow = []
        for y in range(0, 400, 40):
            if not(x == 0 and y == startY):
                rand = random.random()
                if x != 760:
                    if rand < 0.15:
                        tiles.append(tile(x, y, 1))
                        nnTilesRow.append(1)
                        linRegTiles.append(1)
                    elif rand < 0.175:
                        tiles.append(tile(x, y, 2))
                        nnTilesRow.append(-1)
                        linRegTiles.append(-1)
                    else:
                        nnTilesRow.append(0)
                        linRegTiles.append(0)
                else:
                    if not madeAFinish:
                        if rand < (0.7 ** ((400 - x)/40 + 1)):
                            tiles.append(tile(x, y, 3))
                            madeAFinish = True
                            goalX = x + 20
                            goalY = y + 20
                            nnTilesRow.append(2)
                            linRegTiles.append(2)
                        elif rand < (0.7 ** ((400 - x)/40 + 1)) + 0.05:
                            tiles.append(tile(x, y, 1))
                            nnTilesRow.append(1)
                            linRegTiles.append(1)
                        else:
                            nnTilesRow.append(0)
                            linRegTiles.append(0)
                    else:
                        if rand < 0.1:
                            tiles.append(tile(x, y, 1))
                            nnTilesRow.append(1)
                            linRegTiles.append(1)
                        elif rand < 0.11:
                            tiles.append(tile(x, y, 2))
                            nnTilesRow.append(-1)
                            linRegTiles.append(-1)
                        else:
                            nnTilesRow.append(0)
                            linRegTiles.append(0)
            else:
                nnTilesRow.append(0)
                linRegTiles.append(0)
        nnTiles.append(nnTilesRow)
    
    p.x = 0
    p.y = startY * 40
    linRegTiles.append(startY)

def drawTiles():
    for i in tiles:
        i.draw()

def newMap():
    global currentNetwork
    global score
    global timer
    populateTiles()
    currentNetwork = 0
    score = 0
    timer = 0
def loadStage():
    filename = askopenfilename()
    file = open(filename, "r")
    global linRegTiles
    global nnTiles
    global tiles
    global goalX
    global goalY
    global startY
    global currentNetwork
    global score
    global timer
    global minDist
    currentNetwork = 0
    score = 0
    nnTiles = []
    tiles = []
    linRegTiles = []
    startY = random.randint(0, 7)
    for (count, l) in enumerate(file):
        nnTilesRow = []
        line = l.rstrip()
        for i in range(len(line)):
            if line[i] == "1":
                tiles.append(tile(i * 40, count * 40, 1))
                linRegTiles.append(1)
                nnTilesRow.append(1)
            elif line[i] == "2":
                tiles.append(tile(i * 40, count * 40, 2))
                linRegTiles.append(-1)
                nnTilesRow.append(-1)
            elif line[i] == "3":
                tiles.append(tile(i * 40, count * 40, 3))
                linRegTiles.append(2)
                nnTilesRow.append(2)
                goalX = i * 40 + 20
                goalY = count * 40 + 20
            elif line[i] == "S":
                startY = i
                nnTilesRow.append(0)
            else:
                linRegTiles.append(0)
                nnTilesRow.append(0)
        nnTiles.append(nnTilesRow)
    
    p.x = 0
    p.y = startY * 40
    linRegTiles.append(startY)
    nnTiles = Matrix(nnTiles).transpose()
    file.close()
    timer = 0
    minDist = 900
def writeGeneration():
    filename = askopenfilename()
    population.writeGeneration(filename)
def loadGeneration():
    global currentNetwork
    filename = askopenfilename()
    try:
        population.loadGeneration(filename)
        currentNetwork = 0
    except (FileNotFoundError, IOError):
        tkinter.messagebox.showerror("File Not Found",
                                     "The file {0} was not found.".format(
                                         filename))
        quit()
    except:
        tkinter.messagebox.showerror("Error",
                                     "There was a problem reading the file.")
        quit()
    logFile.write("GENERATION {0}\n".format(str(population.generation)))
    gLabel.config(text="Generation: " + str(population.generation))
p = player(0, 0)
currentNetwork = 0
root = Tk()
disp = Canvas(root, width=800, height=400, bg="white")
disp.grid(row=0, column=0, columnspan=2)
gLabel = Label(root, text="Generation: " + str(population.generation))
gLabel.grid(row=1, column=0)
oLabel = Label(root, text="Organism: " + str(currentNetwork))
oLabel.grid(row=1, column=1)
Button(root, text="Write Generation", command=writeGeneration).grid(
    row=2, column=0)
Button(root, text="Load Generation", command=loadGeneration).grid(
    row=2, column=1)
Button(root, text="New Map", command=newMap).grid(row=3, column=0)
Button(root, text="Load Map", command=loadStage).grid(row=3, column=1)

populateTiles()
# print(len(nnTiles))
logFile = open("NLOG.txt", "w")
logFile.write("GENERATION 0\n")
prevScore = 0
minDistInc = 0
gen0File = open("gen0Data.txt", "a")
avgFile = open("avgScores.txt", "a")
def moveLeft(event):
    global moveLeft
    moveLeft = True
def moveRight(event):
    global moveRight
    moveRight = True
def stopLeft(event):
    global moveLeft
    moveLeft = False
def stopRight(event):
    global moveRight
    moveRight = False
if prediction:
    prediction = soothsayer.prediction(linRegTiles)
if playerInput:
    disp.focus_set()
    disp.bind("<Left>", moveLeft)
    disp.bind("<Up>", p.jump)
    disp.bind("<Right>", moveRight)
    disp.bind("<KeyRelease-Left>", stopLeft)
    disp.bind("<KeyRelease-Right>", stopRight)
def main():
    global currentNetwork
    global nnTiles
    global minDist
    global minDistInc
    global score
    global prevScore
    global timer
    global generation
    global logFile
    global startY
    global linRegTiles
    global population
    global prediction
    global soothsayer
##    previousX = copy.copy(p.x)
##    previousY = copy.copy(p.y)
    if drawing:
        disp.delete("all")
        drawTiles()
##    print(p.x, p.y)
##    print(p.xVel, p.yVel)
    # print(len(nnTiles))
##    currentTilePosX = int(p.x // 40)
##    currentTilePosY = int(p.y // 40)
##    print(currentTilePosX)
##    print(currentTilePosY)
    # print(type(currentTilePosX))
    visibleTiles = []
##    try:
##        for i in range(-2, 3):
##            for j in range(-2, 3):
##                visibleTiles.append(
##                    nnTiles[currentTilePosX + i][currentTilePosY + j])
##    except:
##        prevMinDist = copy.copy(minDist)
##        print("\nERROR")
##        print(currentTilePosX + i, currentTilePosY + j)
##        visibleTiles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
##                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
##        p.x = 0
##        p.y = startY * 40
##        minDist = int(minDist * 1.5)
##        minDistInc = 0
##        score -= 50
##        p.xVel = 0
##        p.yVel = 0
    for i in nnTiles:
        for j in i:
            visibleTiles.append(j)
    visibleTiles.append((goalY - 200)/200)
    visibleTiles.append(int(p.jumping))
    visibleTiles.append((p.x - 400)/400)
    visibleTiles.append((p.y - 200)/200)
    visibleTiles.append(p.xVel/5)
    visibleTiles.append(p.yVel/5)
    #print(len(visibleTiles))
    if not playerInput:
        #print(len(visibleTiles))
        result = population.organisms[currentNetwork][0].forwardPropagate(
            copy.deepcopy(visibleTiles))
        #print(result)
        result = result.matrixData[0]
    ##    print(visibleTiles)
    ##    print(result)
        actionNum = max(result)
        action = result.index(actionNum)
    ##    print(action)
        if action == 0:
            p.jump()
        elif action == 1:
            p.moveLeft()
        elif action == 2:
            p.moveRight()
    else:
        if moveLeft:
            p.moveLeft()
        if moveRight:
            p.moveRight()
    p.update()
    prevScore = copy.copy(score)
##    currentX = copy.copy(p.x)
##    currentY = copy.copy(p.y)
    if math.sqrt((goalX - p.x) ** 2 + (goalY - p.y) ** 2) < minDist:
        #score += (minDist - math.sqrt((goalX - p.x) ** 2 + (goalY - p.y) ** 2))
        minDist = copy.copy(math.sqrt(
            (goalX - p.x) ** 2 + (goalY - p.y) ** 2) - 1)
        minDistInc = 1
##    else:
##        if minDist < 250:
##            if timer % 2 == 0:
##                score -= 1
##        elif minDist < 500:
##            score -= 1
##        elif minDist < 750:
##            score -= 2
##        else:
##            score -= 3
##        minDistInc = 0
    if p.finished:
        logFile.write("Organism {0} is a FINISHER!\n".format(
            str(currentNetwork)))
        p.x = 0
        p.y = startY * 40
        score += 1000
        p.finished = False
    if p.dead or p.y > 400:
        p.x = 0
        p.y = startY * 40
        score -= 5
##        minDist = 400 * math.sqrt(5) - 0.5 * minDist
        p.dead = False
        minDistInc = 0
    if drawing:
        disp.create_text(200, 200, text=str(score), fill="blue")
        disp.create_text(200, 210, text=str(timer), fill="red")
        disp.create_text(200, 220, text=str(prediction), fill="#008800")
        disp.create_oval(goalX - minDist, goalY - minDist,
                         goalX + minDist, goalY + minDist, fill="",
                         outline="blue")
                         
    # Next organism
    if timer < timeLimit:
        timer += 1
    else:
        score += int(900 - minDist)
        timer = 0
        p.x = 0
        p.y = startY * 40
        p.xVel = 0
        p.yVel = 0
        p.jumping = True
        minDist = 900
        population.organisms[currentNetwork][1] = score
        print("SCORE FOR ORGANISM", str(currentNetwork), str(score))
        logFile.write("SCORE FOR ORGANISM {0}: {1}\n".format(str(currentNetwork),
                                                           str(score)))
        score = 0
        prevScore = 0
        if currentNetwork < len(population.organisms) - 1:
            currentNetwork += 1
            oLabel.config(text="Organism: " + str(currentNetwork))
        else:
            if population.generation != 0:
                scores = []
                for i in population.organisms:
                    scores.append(i[1])
                adults = scores[:int(len(scores)/2)]
                children = scores[int(len(scores)/2):]
                print("\nAdult Average:", mean(adults))
                print("Child Average:", mean(children))
                print("Mean Growth\n:", mean(children) - mean(adults))
                logFile.write(
                    "\nAdult Score Mean: " + str(mean(adults)) + "\n")
                logFile.write(
                    "Child Score Mean: " + str(mean(children)) + "\n")
                logFile.write(
                    "Mean Growth: " + str(mean(children) - mean(adults)) +\
                    "\n\n")
                print("\nAdult Median:", median(adults))
                print("Child Median:", median(children))
                print("Median Growth\n:", median(children) - median(adults))
                logFile.write(
                    "\nAdult Score Median: " + str(median(adults)) + "\n")
                logFile.write(
                    "Child Score Median: " + str(median(children)) + "\n")
                logFile.write(
                    "Median Growth: " + str(median(children) - median(adults)) +\
                    "\n\n")
                print("\nAdult StDev:", stdev(adults))
                print("Child StDev:", stdev(children))
                print("StDev Difference\n:", stdev(children) - stdev(adults))
                logFile.write(
                    "\nAdult Score Standard Deviation: " + str(stdev(adults)) + \
                    "\n")
                logFile.write(
                    "Child Score Standard Deviation: " + str(stdev(children)) + \
                    "\n")
                logFile.write(
                    "Difference: " + str(stdev(children) - mean(adults)) +\
                    "\n\n")
            else:
                scores = []
                for i in population.organisms:
                    scores.append(i[1])
                if recordGen0:
                    for i in linRegTiles:
                        gen0File.write(str(i) + " ")
                    gen0File.write("\n")
                    gen0File.write(str(mean(scores)) + "\n")
                    if quitGen0:
                        logFile.close()
                        gen0File.close()
                        quit()
                    else:
                        if CONTINUE:
                            population = NNPopulation(
                                26, 13, 206, 3, 1, 0, 0.05, 0.05, 8)
            logFile.write("Difference in prediction: " + \
                          str(mean(scores) - prediction))
            print("Difference in prediction:", mean(scores) - prediction)
            avgFile.write("Average score of Gen. {0}: {1}\n".format(
               str(population.generation), str(mean(scores))))
            gLabel.config(text="Generation: " + str(population.generation))
            logFile.write("GENERATION " + str(population.generation) + "\n")
            currentNetwork = 0
            if switchStage:
                populateTiles()
            if prediction:
                prediction = soothsayer.prediction(linRegTiles)
            if not CONTINUE:
                population.nextGeneration()
                print(len(population.organisms))
            if askWhereTheFileGoes:
                filename = askopenfilename()
                population.writeGeneration(filename)
            else:
                population.writeGeneration("latestGeneration.txt")
    root.after(25, main)

main()
root.mainloop()
logFile.close()
gen0File.close()
avgFile.close()
