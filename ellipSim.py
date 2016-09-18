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

#arrows meant to graphically represent x,y, and z axes
#arrow(axis = vector(1,0,0), length = 25, color = color.blue)
#arrow(axis = vector(0,1,0), length = 25, color = color.blue)
#arrow(axis = vector(0,0,1), length = 25, color = color.blue)

print("Welcome to the cell simulator v2.0")
# numGens = int(input("Please input the number of cell generations you would like to generate: ")) #grab the num gens from user

numGens = 15

# overlapParam = float(input("Please input the maximum amount of overlap permitted before reproduction fails: ")) #grab the overlap parameter from the user

diam = 5.0 #for now all cells will have a diameter of 5, the length will increase each generation if in ellipsoidal mode, in sphere mode it will remain constant

#diamArray = [5.0 + i for i in range(numGens)] #an array of various diameters of the cells to facilitate the change in volume by generation

#diamArray = [(1.0 + (float(i) / numGens)) for i in range(numGens)]

#diamArray = sorted(diamArray, key = lambda x: -x) #the function f(x) = -x causes the list to be sorted in descending order.

diamArray = [5.0 for i in range(numGens)] #having an array of constant diams ensures that all cells are the same size

iterationList = [i for i in range(1, numGens + 1)] #Use this method of looping to assign the cell generations


theta = pi / 4 #this defines the acceptable angles that daughter cells can spawn from
thetaVariance = 0.1 #this is the fraction by which theta may vary at maximum (theta = theta +- random(-1,1)*thetaVariance*theta)

#aspectList = [1.0 + 0.1*i for i in range(11)] #List of aspect ratios to test
#aspectList = [1.1] #right now we only want to execute with one particular aspect ratio


row = 0
col = 0

worksheet.write(row,col, "generation #")
for q in range(20):
    if q % 2 == 0:
        worksheet.write(row,col+1+q, "Cumulative Overlap Trial %d" % (q+1))
    else:
        worksheet.write(row,col+1+q, "Total Rejected Moves Trial %d" % (q+1))

row += 1

overlap_params = [0.10] # [0.10, 0.30, 0.50, 0.70, 0.90]

aspRats = [1.1] # [1.1, 1.2, 1.3, 1.4, 1.5]

param_pairs = [(ov_param, aspRat) for ov_param in overlap_params for aspRat in aspRats]

print "Param Pairs", param_pairs

#HACK get rid of the aspect ratio loop and instead loop over the trial number

#for aspRat in aspectList: #loop over the aspect ratios, to perform a trial at each aspect ratio.

def create_cell_string(cell):
    x,y,z = cell.pos
    axial_x, axial_y, axial_z = cell.axis
    phi = acos(axial_z / mag(cell.axis))
    xy_plane_mag = sqrt(axial_x**2.0 + axial_y**2.0)
    theta = asin(axial_y / xy_plane_mag)
    gen_num = cell.generation
    overlap_amnt = sum(cell.overlaps)
    write_string = '%f, %f, %f, %f, %f, %f, %d' % (x, y, z, theta, phi, overlap_amnt, gen_num)
    return write_string

def output_cell_file(cell_list, filename):
    fh = open(filename, 'w')
    for cell in cell_list:
        cell_string = create_cell_string(cell)
        fh.write(cell_string)
        fh.write('\n')
    fh.close()

for overlapParam, aspRat in param_pairs:

    worksheet.write(row, col+24, 'Overlap Parameter: ')
    worksheet.write(row, col+25, overlapParam)
    worksheet.write(row+1, col+24, 'Aspect Ratio: ')
    worksheet.write(row+1, col+25, aspRat)

    prev_row = row

    for trialNumber in range(10):

        overlaps = 0 #to count the number of overlap cases
        rootCell = RootCell(vector(0,0,0), aspRat*diamArray[0], diamArray[0], vector(1, 2, 3), None, 0) #The original cell, note that it has generation = 0
        cellList.append(rootCell) #put the root cell in the cellList

        start_time = timeit.default_timer()

        for i in iterationList: #iterate over the number of gens

            if trialNumber == 0: #only need to write the generation numbers on the first run-through
                worksheet.write(row,col,i)

            cumulativeOverlap = sum([sum(zell.overlaps) for zell in cellList])

            totalRejectedMoves = sum([zell.failedSpawns for zell in cellList])

            worksheet.write(row, col+1, cumulativeOverlap)

            worksheet.write(row, col+2, totalRejectedMoves)

            row += 1
            # if i != 1:
            #     currText.visible = False
            # currText = text(text='Generation\n' + str(i), align='center', height=10, width=10,pos=vector(50,20,20),depth=-0.3, color=color.green)
            length = aspRat*diamArray[i - 1] #follows from aspRat = length / diam
            temp = []  # holds the newly created cells until the current round of reproduction is over

            # if random.random() <= 0.10:
            #     calling this method switches the pole from which the root cell spawns
            #     rootCell.switchGrowthDirection()

            for cel in cellList: #for each cell currently in the cellList

                #rate(10) #for visual purposes, slow the rate down to see the network grow in real time

                #if random.uniform(0, 1) < doublingProb: #if a randomly generated float in [0,1] is less than the doubling probability, then double

                variedTheta = computeVariedTheta(theta, thetaVariance) #generate a slight random variance in theta to reduce unintended patterns
                (cellPos, direc) = getDaughterPos(cel, variedTheta, length)

                #colTemp = cel.graphical.color
                #cel.graphical.color=color.magenta
                #wait(1)

                if (cellPos,direc) != (None, None):

                    newCell = Cell(cellPos, length, diamArray[i-1], direc, cel, i) #create the daughter

                    ovFail = checkOverlap(newCell, cellList, temp, overlapParam) #check if the daughter overlaps with any existing cells



                    if (not ovFail): #if there is NOT an overlap above the chosen threshold, allow the daughter to exist
                        cel.children.append(newCell) #add it to the children list of its parent
                        temp.append(newCell) #add it to the temporary storage list

                    else:
                        cel.failedSpawns += 1
                        #newCell.graphical.visible = False #make the daughter disappear if it overlapped too much with an existing cell
                        #for sphr in newCell.sphereMesh:
                            #sphr.graphical.visible = False

            for cel in temp: #once the reproduction cycle is complete,

                cellList.append(cel) #add all the newly created daughters in temp to the main cellList

        #exportAsOpenSCAD(cellList, aspectList[0])

        cell_file_name = "overlap_" + str(overlapParam) + "_asprat_" + str(aspRat) +'.txt'

        output_cell_file(cellList, cell_file_name)

        print "Number of Cells:", len(cellList)

        end_time = timeit.default_timer()

        print "Elapsed time:", end_time - start_time

        temp = []
        cellList = [] #if doing multiple trials, we need to reset these arrays before starting the next trial
        col += 2 #move the excel coordinate one column over for the next trial
        row = prev_row #row coordinate goes back to just below the columnt titles

    row += numGens + 2
    col = 0

workbook.close()

sys.exit() #if this is uncommented the program will exit when it is finished running, you wont have time to view the visual representation of the cluster
#it's mostly only used when collecting data and not using the visual mode
