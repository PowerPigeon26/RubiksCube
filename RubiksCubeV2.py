########################################################################################################
#SUMMARY: v2 removes all unnecessary lines and calculation, just finds and save rotations needed and 
#         how many times multiple sides completed.
########################################################################################################
#REQUIRED LIBRARIES
import random
import copy
import os
########################################################################################################
#CUBE CREATION

#Creates a list containing all six sides of a Rubik's cube of a given size
def CreateRubiksCube(size):

    RubiksCube = []
    for i in range(6):
        rubiksSide = CreateRubiksSideList(size, i)
        RubiksCube.append(rubiksSide)
    
    return RubiksCube

#Creates 1 side of the Rubik's Cube of a given size with a particular value "filler" for each element
def CreateRubiksSideList(size, filler):

    endList = []
    for i in range(size):
        row = [filler] * size
        endList.append(row)

    return endList

########################################################################################################
#ROTATE FACE OF CUBE

#Rotates the side of the cube
def rotateSquareMatrix(matrix, rotDir):
    
    rotatedMatrix = copy.deepcopy(matrix)
    size = len(matrix)
    if rotDir == 0:    #clockwise
        for i in range(size):
            for j in range(size):
                rotatedMatrix[j][(size-1)-i] = matrix[i][j]

    if rotDir == 1:    #counter-clockwise
        for i in range(size):
            for j in range(size):
                rotatedMatrix[j][i] = matrix[i][(size-1) - j]
    
    #print(rotatedMatrix)
    return rotatedMatrix

########################################################################################################
#MANIPULATE CUBE [[front][right][back][left][top][bottom]]
#note: XYZ, left to right, bottom to top, back to front. typeOfTurn = (where on cube, turn direction)

#Determine what random rotation should be committed
def DetermineRotationType(size):
    rotationLocationsTotal = size * 3
    rotationLocationRaw = random.randint(0,rotationLocationsTotal-1)
    rotationSide = rotationLocationRaw // size
    rotationLocation = rotationLocationRaw % size
    typeOfTurn = (rotationSide, rotationLocation, random.randint(0,1))

    return typeOfTurn

#Perform turn on x-axis
def XAxisTurn(rubiksCube, size, rotationLocation, rotDir):
    
    newCube = copy.deepcopy(rubiksCube)
    #ROTATE UP
    if rotDir == 0: # Seems to work for 3x3, untested on 4x4
        for i in range(size):
            newCube[0][i][rotationLocation] = rubiksCube[5][i][rotationLocation]
            newCube[4][i][rotationLocation] = rubiksCube[0][i][rotationLocation]
            newCube[2][i][(size-1) - rotationLocation] = rubiksCube[4][(size-1) - i][rotationLocation]
            newCube[5][i][rotationLocation] = rubiksCube[2][(size-1) - i][(size-1) - rotationLocation]
        if rotationLocation == 0:
            newCube[3] = rotateSquareMatrix(newCube[3], 1)
        if rotationLocation == size-1:
            newCube[1] = rotateSquareMatrix(newCube[1], 0)


    #ROTATE DOWN
    if rotDir == 1: # Seems to work for 3x3, untested on 4x4
        for i in range(size):
            newCube[0][i][rotationLocation] = rubiksCube[4][i][rotationLocation]
            newCube[4][(size-1) - i][rotationLocation] = rubiksCube[2][i][(size-1) - rotationLocation]
            newCube[2][(size-1) - i][(size-1) - rotationLocation] = rubiksCube[5][i][rotationLocation]
            newCube[5][i][rotationLocation] = rubiksCube[0][i][rotationLocation]
        if rotationLocation == 0:
            newCube[3] = rotateSquareMatrix(newCube[3], 0)
        if rotationLocation == size-1:
            newCube[1] = rotateSquareMatrix(newCube[1], 1)

    return newCube

#Perform turn on y-axis
def YAxisTurn(rubiksCube, size, rotationLocation, rotDir):
    
    newCube = copy.deepcopy(rubiksCube)
    #ROTATE RIGHT
    if rotDir == 0:
        for i in range(size):
            newCube[0][(size-1) - rotationLocation][i] = rubiksCube[3][(size-1) - rotationLocation][i]
            newCube[1][(size-1) - rotationLocation][i] = rubiksCube[0][(size-1) - rotationLocation][i]
            newCube[2][(size-1) - rotationLocation][i] = rubiksCube[1][(size-1) - rotationLocation][i]
            newCube[3][(size-1) - rotationLocation][i] = rubiksCube[2][(size-1) - rotationLocation][i]
        if rotationLocation == 0:
            newCube[5] = rotateSquareMatrix(newCube[5], 0)
        if rotationLocation == size-1:
            newCube[4] = rotateSquareMatrix(newCube[4], 1)

    #ROTATE LEFT
    if rotDir == 1:
        for i in range(size):
            newCube[0][(size-1) - rotationLocation][i] = rubiksCube[1][(size-1) - rotationLocation][i]
            newCube[1][(size-1) - rotationLocation][i] = rubiksCube[2][(size-1) - rotationLocation][i]
            newCube[2][(size-1) - rotationLocation][i] = rubiksCube[3][(size-1) - rotationLocation][i]
            newCube[3][(size-1) - rotationLocation][i] = rubiksCube[0][(size-1) - rotationLocation][i]
        if rotationLocation == 0:
            newCube[5] = rotateSquareMatrix(newCube[5], 1)
        if rotationLocation == size-1:
            newCube[4] = rotateSquareMatrix(newCube[4], 0)

    return newCube

#Perform turn on Z-axis
def ZAxisTurn(rubiksCube, size, rotationLocation, rotDir):
    
    newCube = copy.deepcopy(rubiksCube)
    #ROTATE RIGHT
    if rotDir == 0:
        for i in range(size):
            newCube[1][i][rotationLocation] = rubiksCube[4][(size-1) - rotationLocation][i]
            newCube[4][(size-1) - rotationLocation][i] = rubiksCube[3][(size-1) - i][(size-1) - rotationLocation]
            newCube[3][i][(size-1) - rotationLocation] = rubiksCube[5][rotationLocation][i]
            newCube[5][rotationLocation][i] = rubiksCube[1][(size-1) - i][rotationLocation]
        if rotationLocation == 0:
            newCube[0] = rotateSquareMatrix(newCube[0], 0)
        if rotationLocation == size-1:
            newCube[2] = rotateSquareMatrix(newCube[2], 1)

    #ROTATE LEFT
    if rotDir == 1:
        for i in range(size):
            newCube[1][(size-1) - i][rotationLocation] = rubiksCube[5][rotationLocation][i]
            newCube[5][rotationLocation][i] = rubiksCube[3][i][(size-1) - rotationLocation]
            newCube[3][(size-1) - i][(size-1) - rotationLocation] = rubiksCube[4][(size-1) - rotationLocation][i]
            newCube[4][(size-1) - rotationLocation][i] = rubiksCube[1][i][rotationLocation]
        if rotationLocation == 0:
            newCube[0] = rotateSquareMatrix(newCube[0], 1)
        if rotationLocation == size-1:
            newCube[2] = rotateSquareMatrix(newCube[2], 0)

    return newCube

#Go to either x, y, or z based on typeOfTurn[0]
def PerformRotation(rubiksCube, size, typeOfTurn):

    if typeOfTurn[0] == 0:
        rubiksCube = XAxisTurn(rubiksCube, size, typeOfTurn[1], typeOfTurn[2])

    if typeOfTurn[0] == 1:
        rubiksCube = YAxisTurn(rubiksCube, size, typeOfTurn[1], typeOfTurn[2])

    if typeOfTurn[0] == 2:
        rubiksCube = ZAxisTurn(rubiksCube, size, typeOfTurn[1], typeOfTurn[2])
    
    return rubiksCube

#Call to perform a random rotation on a cube
def PerformRandomRotation(rubiksCube, size):

    typeOfTurn = DetermineRotationType(size)
    rubiksCube = PerformRotation(rubiksCube, size, typeOfTurn)
    return rubiksCube

#Prints cube to console
def PrintCube(rubiksCube, size):
    for i in range(6):
        print('---------------')
        for j in range(size):
            print(rubiksCube[i][j])

#Checks if cube is fixed, true if each side has only one number, else fales
def CubeIsStable2(rubiksCube, size):

    global numberOfSidesCompleted

    successCounter = 0
    for i in range(len(rubiksCube)):
        checkSidesValues = []
        for j in range(size):
            checkSidesValues = checkSidesValues + rubiksCube[i][j]
        checkSidesValues = list(set(checkSidesValues))
        if len(checkSidesValues) == 1:
            successCounter += 1
    
    if successCounter > 0:
        numberOfSidesCompleted[successCounter - 1] += 1
    if successCounter != 6:
        return False
    else:
        return True

def SaveResults(size, randomRotationsCompleted, successOrNo, filename):

    global numberOfSidesCompleted
    global initialRandomRotations

    '''
    #DETAILED OUTPUT
    if os.path.exists(filename + ".txt") == False:
        RubiksResults = open(filename + ".txt", "w")
        RubiksResults.close()

    RubiksResults = open(filename + ".txt", "a")
    RubiksResults.write(str(size) + "x" + str(size) + " Rubik's Cube " + str(successOrNo) + " " + str(randomRotationsCompleted) + " random rotations! ("
                         + str(initialRandomRotations) + " random rotations used to initialize)\n")
    RubiksResults.write("How many times 1 or more sides are completed: " + str(numberOfSidesCompleted) + "\n\n")
    RubiksResults.close()
    '''
    
    #RAW DATA OUTPUT
    if os.path.exists(filename + "Raw.txt") == False:
        RubiksResults = open(filename + "Raw.txt", "w")
        RubiksResults.close()
    
    RubiksResults = open(filename + "Raw.txt", "a")
    RubiksResults.write(str(randomRotationsCompleted) + "\n")
    RubiksResults.write(str(numberOfSidesCompleted) + "\n")
    RubiksResults.close()

########################################################################################################
#RUN THE CODE

#TOTAL CUBES TO TRY AND FIX
totalTrials = 10
trials = 0
while trials < totalTrials:
    
    #CONDITIONS OF TRIALS, VARIABLE
    size = 2
    initialRandomRotations = 1000
    #rotationLimit = 10000           #10 thousand, for tests
    #rotationLimitString = "10Thou"
    #rotationLimit = 1000000         #1 million
    #rotationLimitString = "1Mil"
    #rotationLimit = 10000000        #10 million
    #rotationLimitString = "10Mil"
    rotationLimit = 1000000000      #1 billion, good for true tests
    rotationLimitString = "1Bil"
    #rotationLimit = 10000000000      #10 billion, good for true tests
    #rotationLimitString = "10Bil"

    #CONDITIONS OF TRIALS, CONSTANTS
    randomRotationsCompleted = 0
    numberOfSidesCompleted = [0] * 6
    printCounter = 0
    filename = str(size) + "x" + str(size) + "RubiksCube" + rotationLimitString
    printPercent = rotationLimit / 10000

    #CREATE CUBE OF SIZE 2 OR MORE UNITS
    rubiksCube = CreateRubiksCube(size)

    #INITIAL RANDOM ROTATIONS, ROTATE AGAIN IF STILL STABLE
    while CubeIsStable2(rubiksCube, size) == True:
        for i in range(initialRandomRotations):
            rubiksCube = PerformRandomRotation(rubiksCube, size)

    #RESET THIS DUE TO RANDOM ROTATIONS AFFECTING IT
    numberOfSidesCompleted = [0] * 6

    #RANDOMLY ROTATE UNTIL IT IS DONE *DOOM MUSIC* (OR ROTATION LIMIT REACHED)
    stable = False
    while stable == False and randomRotationsCompleted < rotationLimit:
        rubiksCube = PerformRandomRotation(rubiksCube, size)
        randomRotationsCompleted += 1
        stable = CubeIsStable2(rubiksCube, size)
        printCounter += 1
        if printCounter >= printPercent:
            os.system('cls')
            printCounter = 0
            print(trials+1)
            print(round((randomRotationsCompleted/rotationLimit)*100, 2))

    #SAVE RESULTS
    if randomRotationsCompleted >= rotationLimit:
        SaveResults(size, randomRotationsCompleted, "was NOT saved after", filename)
    else:
        SaveResults(size, randomRotationsCompleted, "was saved after", filename)

    #INCREMENT trials BY ONE
    trials += 1
    

