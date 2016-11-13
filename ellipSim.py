from visual import *
from math import *
from cell import *
from cellHelper import *
import xlsxwriter as xls
import sys
import timeit


__author__ = "Elyes Graba"
__credits__ = ["Peter Yunker", "Shane Jacobeen"]
__version__ = "3.0.1"
__maintainer__ = "Elyes Graba"
__email__ = "elyesgraba@gatech.edu"
__status__ = "Development"

#Globals
cellList = [] #a list of all the cell objects that currently exist

#NOTE unused currently, no need for reproduction probablility
doublingProb = 0.95 #for now we use a hard-coded doubling probability of 95%

workbook = xls.Workbook(sys.argv[1])
worksheet = workbook.add_worksheet()

print("Welcome to the cell simulator v2.0")

numGens = 15

diam = 5.0 #for now all cells will have a diameter of 5, the length will increase each generation if in ellipsoidal mode, in sphere mode it will remain constant

iterationList = [i for i in range(1, numGens + 1)] #Use this method of looping to assign the cell generations


theta = pi / 4 #this defines the acceptable angles that daughter cells can spawn from
thetaVariance = 0.1 #this is the fraction by which theta may vary at maximum (theta = theta +- random(-1,1)*thetaVariance*theta)


row = 0
col = 0

worksheet.write(row,col, "generation #")
for q in range(100):
    worksheet.write(row,3*q+1, "Cumulative Overlap Trial %d" % (q))
    worksheet.write(row,3*q+2, "Total Rejected Moves Trial %d" % (q))
    worksheet.write(row,3*q + 3, "Cumulative Squared Overlap Trial %d" % (q))

row += 1

overlap_params = [0.50]  # [0.10, 0.30, 0.50, 0.70, 0.90]

filenames_for_ARs = ["week_1_ARs.csv", "week_8_ARs.csv"]

AR_distributions = build_aspect_ratio_distributions(filenames_for_ARs)

distribution = AR_distributions[0]

for overlapParam in overlap_params:

    prev_row = row

    for trialNumber in range(100):

        if trialNumber == 50:
            distribution = AR_distributions[1]

        overlaps = 0 #to count the number of overlap cases
        rootCell = RootCell(vector(0,0,0), select_aspect_ratio(distribution)*diam, diam, vector(1, 2, 3), None, 0) #The original cell, note that it has generation = 0
        cellList.append(rootCell) #put the root cell in the cellList

        for i in iterationList: #iterate over the number of gens

            if trialNumber == 0: #only need to write the generation numbers on the first run-through
                worksheet.write(row, col, i)

            cumulativeOverlap = sum([sum(zell.overlaps) for zell in cellList])

            totalRejectedMoves = sum([zell.failedSpawns for zell in cellList])

            cumulativeSquaredOverlap = sum([sum(zell.overlaps)**2 for zell in cellList])

            worksheet.write(row, col+1, cumulativeOverlap)

            worksheet.write(row, col+2, totalRejectedMoves)

            worksheet.write(row, col+3, cumulativeSquaredOverlap)

            row += 1

            length = select_aspect_ratio(distribution)*diam #follows from aspRat = length / diam
            temp = []  # holds the newly created cells until the current round of reproduction is over

            for cel in cellList: #for each cell currently in the cellList

                variedTheta = computeVariedTheta(theta, thetaVariance) #generate a slight random variance in theta to reduce unintended patterns
                (cellPos, direc) = getDaughterPos(cel, variedTheta, length)

                if (cellPos,direc) != (None, None):

                    newCell = Cell(cellPos, length, diam, direc, cel, i) #create the daughter

                    ovFail = checkOverlap(newCell, cellList, temp, overlapParam) #check if the daughter overlaps with any existing cells

                    if (not ovFail): #if there is NOT an overlap above the chosen threshold, allow the daughter to exist
                        cel.children.append(newCell) #add it to the children list of its parent
                        temp.append(newCell) #add it to the temporary storage list

                    else:
                        cel.failedSpawns += 1
                        # newCell.graphical.visible = False #make the daughter disappear if it overlapped too much with an existing cell
                        # for sphr in newCell.sphereMesh:
                        #     sphr.graphical.visible = False

            for cel in temp: #once the reproduction cycle is complete,

                cellList.append(cel) #add all the newly created daughters in temp to the main cellList


        temp = []
        cellList = [] #if doing multiple trials, we need to reset these arrays before starting the next trial
        col += 3
        row = prev_row #row coordinate goes back to just below the columnt titles

    row += numGens + 2
    col = 0

workbook.close()

sys.exit() #if this is uncommented the program will exit when it is finished running, you wont have time to view the visual representation of the cluster
#it's mostly only used when collecting data and not using the visual mode
