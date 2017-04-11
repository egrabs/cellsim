from visual import *
from math import *
from cell import *
from cellHelper import *
import sys
from timeit import default_timer
import threading as td


__author__ = "Elyes Graba"
__credits__ = ["Peter Yunker", "Shane Jacobeen"]
__version__ = "3.0.1"
__maintainer__ = "Elyes Graba"
__email__ = "elyesgraba@gatech.edu"
__status__ = "Development"


MAX_NUM_THREADS = 10
NUM_TRIALS = 100

AR_distribution_filenames = ["week1ArDistribution.txt", "week4ArDistribution.txt", "week8ArDistribution.txt"]
dist_names = ['week1', 'week4', 'week8']
AR_distributions = build_aspect_ratio_distributions(AR_distribution_filenames)

print "AR DISTRIBUTIONS: ", AR_distributions

AR_distributions = zip(dist_names, AR_distributions)

print "AR DISTRIBUTIONS AFTER ZIP", AR_distributions

# generates the cases that go into the data (AKA one line in the .csv)
def generate_case(cellList=None, generation=0):
    if ( (cellList==None) or (generation==0) ):
        return 'GENERATION, CUMULATIVE_OVERLAP, NUM_REJECTED_MOVES, CUMULATIVE_SQUARED_OVERLAP\n'
    else:
        cumulativeOverlap = sum([sum(cell.overlaps) for cell in cellList])
        totalRejectedMoves = sum([cell.failedSpawns for cell in cellList])
        cumulativeSquaredOverlap = sum([sum(cell.overlaps)**2 for cell in cellList])
        return '%d, %f, %f, %f\n' % (generation, cumulativeOverlap, totalRejectedMoves, cumulativeSquaredOverlap)


def run_cluster(distributionNameAndVals, trial_num):

    start_time = default_timer()

    name, distribution = distributionNameAndVals

    dataFilename = "data_files/" + name + "_distribution_trial_" + str(trial_num) + '_data_file.csv'
    fh = open(filename, 'w')
    headers = generate_case()
    fh.write(headers)

    volume = 98.0
    overlapParam = 0.50
    theta = pi / 4.
    numGens = 12

    cellList = []

    aspectRatio = select_aspect_ratio(distribution=distribution)
    minorAxis, majorAxis = getCellDimensions(aspectRation=aspectRatio, volume=volume)
    length = 2*majorAxis
    diam = 2*minorAxis
    rootCell = RootCell(pos=vector(0,0,0), length=length, diameter=diam, axis=vector(1, 2, 3), parent=None, generation=0) #The original cell, note that it has generation = 0
    cellList.append(rootCell) #put the root cell in the cellList

    for i in range(1, numGens + 1): #iterate over the number of gens

        temp = []  # holds the newly created cells until the current round of reproduction is over

        for cel in cellList: #for each cell currently in the cellList

            aspectRatio = select_aspect_ratio(distribution=distribution)
            minorAxis, majorAxis = getCellDimensions(aspectRatio=aspectRatio, volume=volume)
            length = 2.*majorAxis
            diam = 2.*minorAxis

            variedTheta = computeVariedTheta(theta=theta, variance=thetaVariance) #generate a slight random variance in theta to reduce unintended patterns
            
            # length is the length of the daughter
            # which may have a different aspect ratio
            # and therefore a different length
            # than its parent
            (cellPos, direc) = getDaughterPos(cel=cel, theta=variedTheta, length=length)

            if (cellPos, direc) != (None, None):

                newCell = Cell(pos=cellPos, length=length, diameter=diam, axis=direc, parent=cel, generation=i) #create the daughter
                ovFail = checkOverlap(currCell=newCell, cellList=cellList, temp=temp, overlapAmnt=overlapParam) #check if the daughter overlaps with any existing cells

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

        case = generate_case(cellList=cellList, generation=i)
        fh.write(case)

    fh.close()

    clusterFileName = "cluster_files/" + name + "_distribution_trial_" + str(trial_num) + '_cluster_file.csv'
    output_cell_file(clusterFileName, cell_file_name)

    # explicitly clear these to save memory sooner
    temp = []
    cellList = [] 

    end_time = default_timer()

    print "trial " + str(trialNumber) + " complete of " + str(NUM_TRIALS)
    print "with an elapsed time of: " + str(end_time - start_time) + " seconds\n"
    return




for distribution in AR_distributions:
    for trial_num in range(1,NUM_TRIALS):
        while True:
            # loop until a thread terminates and we have room to spawn another
            if td.active_count() < MAX_NUM_THREADS:
                thread = td.Thread(group=None, target=run_cluster, name=None, args=(distribution, trial_num), kwargs={})
                thread.start()
                break

while True:
    # loop until all threads terminate, then we can exit
    # the original process itself counts as a thread
    # so we are done when there is exactly one thread running
    if td.active_count() == 1:
        sys.exit(0)
