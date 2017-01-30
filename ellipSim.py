from visual import *
from math import *
from cell import *
from cellHelper import *
import xlsxwriter as xls
from multiprocessing import Process
import numpy as np
import random
from random import gauss

__author__ = "Elyes Graba"
__credits__ = ["Peter Yunker", "Shane Jacobeen"]
__version__ = "3.0.1"
__maintainer__ = "Elyes Graba"
__email__ = "elyesgraba@gatech.edu"
__status__ = "Development"


#Globals
cellList = [] #a list of all the cell objects that currently exist

#NOTE unused currently, no need for reproduction probablility
doublingProb = 0.50 #for now we use a hard-coded doubling probability

#arrows meant to graphically represent x,y, and z axes
#arrow(axis = vector(1,0,0), length = 25, color = color.blue)
#arrow(axis = vector(0,1,0), length = 25, color = color.blue)
#arrow(axis = vector(0,0,1), length = 25, color = color.blue)

print("Welcome to the cell simulator v2.0")
# numGens = int(input("Please input the number of cell generations you would like to generate: ")) #grab the num gens from user

numGens = 3

overlapParam = 0.50  # float(input("Please input the maximum amount of overlap permitted before reproduction fails: ")) #grab the overlap parameter from the user

diam = 5.0 #for now all cells will have a diameter of 5, the length will increase each generation if in ellipsoidal mode, in sphere mode it will remain constant

iterationList = [i for i in range(1, numGens + 1)] #Use this method of looping to assign the cell generations

theta = pi / 4 #this defines the acceptable angles that daughter cells can spawn from
thetaVariance = 0.1 #this is the fraction by which theta may vary at maximum (theta = theta +- random(-1,1)*thetaVariance*theta)

overlaps = 0 #to count the number of overlap cases

# if sim_mode is True, lightweight, data-oriented cell representations will be used and visual output will be supressed
sim_mode = True if raw_input("Run in sim mode? (faster with no visual rendering) enter y/n") == 'y' else False


#aspect ratio disitrbution means
AR_dist_means = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
#aspect ratio distribution standard deviations
AR_dist_STDEVs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]

# angle of attachment distribution means
AoA_means = ['pi / 6.', 'pi / 5.', 'pi / 4.', 'pi / 3.', 'pi / 2.']
# angle of attachment distribution standard deviations will be computed "live"
# by multiplying these fractional values times the actual AoA value
AoA_fractional_STDEVs = [0.0, 0.05, 0.10, 0.15, 0.20]

overlap_squared_threshold = 603504.


row = 0
col = 0



row += 1

AoA_STDEV = 0.0
AR_STDEV = 0.0

for mean_AR in AR_dist_means:
    for mean_AoA in AoA_means:

        text_AoA = mean_AoA

        mean_AoA = eval(mean_AoA)

        AoA_gen = build_distribution_generator(mean_AoA, AoA_STDEV)
        AR_gen = build_distribution_generator(mean_AR, AR_STDEV)

        for trial_num in range(20):

            worksheet.write(row, col, "Cell #")
            worksheet.write(row, col+1, "Angle of Attachment")
            worksheet.write(row, col+2, "Aspect Ratio")
            worksheet.write(row, col+3, "Number of Cells")
            worksheet.write(row, col+4, "Cumulative Overlap")
            worksheet.write(row, col+5, "Cumulative Squared Overlap")
            worksheet.write(row, col+6, "Max overlap of Single Cell")
            worksheet.write(row, col+7, "Generation #")

            worksheet.write(row, col, curr_numcells - 1)  # the cell number (rootcell is 0)
            worksheet.write(row, col+1, text_AoA)
            worksheet.write(row, col+2, mean_AR)
            worksheet.write(row, col+3, curr_numcells)
            worksheet.write(row, col+4, cumulativeOverlap)
            worksheet.write(row, col+5, cumulativeSquaredOverlap)
            worksheet.write(row, col+7, generation)

            generation = 0

            if sim_mode:
                rootCell = construct_lightweight_cell_repr(vector(0,0,0), AR_gen.poll()*diam, diam, vector(1,2,3))
            else:
                rootCell = RootCell(vector(0,0,0), AR_gen.poll()*diam, diam, vector(1, 2, 3), None, 0) #The original cell, note that it has generation = 0

            cellList.append(rootCell) #put the root cell in the cellList

            not_done = True

            while not_done: #iterate until the max overlap threshold is reached

                generation += 1

                temp = [] #holds the newly created cells until the current round of reproduction is over

                for cel in cellList: #for each cell currently in the cellList


                    length = AR_gen.poll()*diam 

                    variedTheta = AoA_gen.poll()
                    (cellPos, direc) = getDaughterPos(cel, variedTheta, length)

                    if (cellPos,direc) != (None, None):

                        if sim_mode:
                            newCell = construct_lightweight_cell_repr(cellPos, length)
                        else:
                            newCell = Cell(cellPos, length, diam, direc, cel, generation) #create the daughter

                        ovFail = checkOverlap(newCell, cellList, temp, overlapParam) #check if the daughter overlaps with any existing cells

                        if (not ovFail): #if there is NOT an overlap above the chosen threshold, allow the daughter to exist
                            if not sim_mode:
                                cel.children.append(newCell) #add it to the children list of its parent
                            temp.append(newCell) #add it to the temporary storage list

                            cumulativeOverlap = sum([sum(zell.overlaps) for zell in cellList])
                            cumulativeSquaredOverlap = sum([sum(zell.overlaps)**2 for zell in cellList])
                            curr_numcells = len(cellList) + len(temp)
                            worksheet.write(row, col, curr_numcells - 1)  # the cell number (rootcell is 0)
                            worksheet.write(row, col+1, text_AoA)
                            worksheet.write(row, col+2, mean_AR)
                            worksheet.write(row, col+3, curr_numcells)
                            worksheet.write(row, col+4, cumulativeOverlap)
                            worksheet.write(row, col+5, cumulativeSquaredOverlap)
                            worksheet.write(row, col+7, generation)
                            if len(temp) > 0:
                                worksheet.write(row, col+6, max([sum(max(cellList, key=lambda cell:sum(cell.overlaps)).overlaps), sum(max(temp, key=lambda cell: sum(cell.overlaps)).overlaps)]))
                            else:
                                worksheet.write(row, col+6, sum(max(cellList, key=lambda cell:sum(cell.overlaps)).overlaps))
                            row += 1

                        else:
                            cel.failedSpawns += 1
                            # if not sim_mode:
                                # newCell.graphical.visible = False #make the daughter disappear if it overlapped too much with an existing cell

                    cumulativeOverlap = sum([sum(zell.overlaps) for zell in cellList])
                    cumulativeSquaredOverlap = sum([sum(zell.overlaps)**2 for zell in cellList])

                    if cumulativeSquaredOverlap >= current_treshold:
                        checker_index += 1
                        if checker_index == len(cumulative_squared_overlap_thresholds):
                            not_done = False
                            break
                        else:
                            print "CHECKER INDEX:", checker_index
                            print "length of threshold array:", len(cumulative_squared_overlap_thresholds)
                            current_treshold = cumulative_squared_overlap_thresholds[checker_index]
                            worksheet.write(row, col, mean_AoA)
                            worksheet.write(row, col+1, mean_AR)
                            worksheet.write(row, col+2, len(cellList) + len(temp))
                            worksheet.write(row, col+3, cumulativeOverlap)
                            worksheet.write(row, col+4, cumulativeSquaredOverlap)
                            if len(temp) > 0:
                                worksheet.write(row, col+5, max([sum(max(cellList, key=lambda cell:sum(cell.overlaps)).overlaps), sum(max(temp, key=lambda cell: sum(cell.overlaps)).overlaps)]))
                            else:
                                worksheet.write(row, col+5, sum(max(cellList, key=lambda cell:sum(cell.overlaps)).overlaps))
                            row += 1

                for cel in temp: #once the reproduction cycle is complete,
                    cellList.append(cel) #add all the newly created daughters in temp to the main cellList


            temp = []
            cellList = [] #if doing multiple trials, we need to reset these arrays before starting the next trial

workbook.close()

sys.exit()

#if this is uncommented the program will exit when it is finished running, you wont have time to view the visual representation of the cluster
#it's mostly only used when collecting data and not using the visual mode
