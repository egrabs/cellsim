from visual import *
from math import *
from cell import *
from cellHelper import *
import xlsxwriter as xls
import numpy as np
import random
from random import gauss
import sys
import threading as td

__author__ = "Elyes Graba"
__credits__ = ["Peter Yunker", "Shane Jacobeen"]
__version__ = "3.0.1"
__maintainer__ = "Elyes Graba"
__email__ = "elyesgraba@gatech.edu"
__status__ = "Development"


#Globals

#NOTE unused currently, no need for reproduction probablility
doublingProb = 0.50 #for now we use a hard-coded doubling probability

print("Welcome to the cell simulator v2.0")

overlapParam = 0.50  # float(input("Please input the maximum amount of overlap permitted before reproduction fails: ")) #grab the overlap parameter from the user

diam = 5.0 #for now all cells will have a diameter of 5, the length will increase each generation if in ellipsoidal mode, in sphere mode it will remain constant

# iterationList = [i for i in range(1, numGens + 1)] #Use this method of looping to assign the cell generations

# theta = pi / 4 #this defines the acceptable angles that daughter cells can spawn from

overlaps = 0 #to count the number of overlap cases

# if sim_mode is True, lightweight, data-oriented cell representations will be used and visual output will be supressed
sim_mode = True if raw_input("Run in sim mode? (faster with no visual rendering) enter y/n: ") == 'y' else False


#aspect ratio disitrbution means
AR_dist_means = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
#aspect ratio distribution standard deviations
AR_dist_STDEVs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]

# angle of attachment distribution means
AoA_means = ['pi/6.', 'pi/5.', 'pi/4.', 'pi/3.', 'pi/2.']
# angle of attachment distribution standard deviations will be computed "live"
# by multiplying these fractional values times the actual AoA value
AoA_fractional_STDEVs = [0.0, 0.05, 0.10, 0.15, 0.20]

# taken from averages at 12 generations with AR = 1.5 and AoA = pi / 4.
overlap_squared_threshold = 603504.

AoA_STDEV = 0.0
AR_STDEV = 0.0

# nvm, I don't think this is needed because threads close themselves when their entered function returns

# class is_done:
    
#     def __init__(self):
#         self.done = False

# done = is_done()

                


def main(mean_AR, mean_AoA, trial_num):

    text_AoA = mean_AoA

    mean_AoA = eval(mean_AoA)

    STDEV = 0.0

    AoA_gen = build_distribution_generator(mean_AoA, STDEV)
    AR_gen = build_distribution_generator(mean_AR, STDEV)

    cellList = [] #a list of all the cell objects that currently exist

    csv_name = 'AR_%f_AoA_%f_trial_%d.csv' % (mean_AR, mean_AoA, trial_num)

    fh = open(csv_name, 'w')

    fh.write('cell_#,angle_of_attachment,aspect_ratio,number_of_cells,cumulative_overlap,cumulative_squared_overlap,max_overlap_of_single_cell,generation_#\n')

    generation = 0

    if sim_mode:
        rootCell = construct_lightweight_cell_repr(vector(0,0,0), AR_gen.poll()*diam, diam, vector(1,2,3))
    else:
        rootCell = RootCell(vector(0,0,0), AR_gen.poll()*diam, diam, vector(1, 2, 3), None, 0) #The original cell, note that it has generation = 0

    cellList.append(rootCell) #put the root cell in the cellList

    initial_case = '0,%f,%f,1,0,0,0,0\n' % (mean_AoA, mean_AR)
    fh.write(initial_case)

    done = False

    while not done: #iterate until the max overlap threshold is reached

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
                    if len(temp) > 0:
                        max_single_cell_overlap = max([sum(max(cellList, key=lambda cell:sum(cell.overlaps)).overlaps), sum(max(temp, key=lambda cell: sum(cell.overlaps)).overlaps)])
                    else:
                        max_single_cell_overlap = sum(max(cellList, key=lambda cell:sum(cell.overlaps)).overlaps)
                    cumulativeOverlap = sum([sum(zell.overlaps) for zell in cellList])
                    cumulativeSquaredOverlap = sum([sum(zell.overlaps)**2 for zell in cellList])
                    curr_numcells = len(cellList) + len(temp)
                    case = '%d,%f,%f,%d,%f,%f,%f,%d\n' % (curr_numcells - 1, mean_AoA, mean_AR, curr_numcells, cumulativeOverlap, cumulativeSquaredOverlap, max_single_cell_overlap, generation)
                    fh.write(case)

                else:
                    cel.failedSpawns += 1
                    # if not sim_mode:
                        # newCell.graphical.visible = False #make the daughter disappear if it overlapped too much with an existing cell

            cumulativeOverlap = sum([sum(zell.overlaps) for zell in cellList])
            cumulativeSquaredOverlap = sum([sum(zell.overlaps)**2 for zell in cellList])

            if cumulativeSquaredOverlap >= overlap_squared_threshold:
                done = True
                fh.close()
                break

        for cel in temp: #once the reproduction cycle is complete,
            cellList.append(cel) #add all the newly created daughters in temp to the main cellList

    temp = []
    cellList = [] #if doing multiple trials, we need to reset these arrays before starting the next trial

    return


for mean_AR in AR_dist_means:
    for mean_AoA in AoA_means:
        for trial_num in range(1,101):
            while True:
                # loop until a thread terminates and we have room to spawn another
                if td.active_count() < 30:
                    thread = td.Thread(group=None, target=main, name=None, args=(mean_AR, mean_AoA, trial_num), kwargs={})
                    thread.start()
                    break

while True:
    # loop until all threads terminate, then we can exit
    if td.active_count() == 0:
        sys.exit(0)

