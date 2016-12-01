from visual import *
from math import *
import os
import random
from cell import *

__author__ = "Elyes Graba"
__credits__ = ["Peter Yunker", "Shane Jacobeen"]
__version__ = "3.0.1"
__maintainer__ = "Elyes Graba"
__email__ = "elyesgraba@gatech.edu"
__status__ = "Development"

def exportAsOpenSCAD(cellList, aspectRatio):

    fileNumber = 0
    for fileName in os.listdir(os.getcwd()):
        if "ellipsoidNetwork" in fileName:
            if int(fileName[len("ellipsoidNetwork")]) >= fileNumber:
                fileNumber = int(fileName[len("ellipsoidNetwork")]) + 1

    fileName = "ellipsoidNetwork" + str(fileNumber) + ".scad"

    fh = open(fileName, 'w')

    for cell in cellList:


        (xPos, yPos, zPos) = cell.pos

        rotationalAxis = cross(vector(0,0,1), cell.axis)

        angleToRotateRad = acos(dot(vector(0,0,1), norm(cell.axis))) #python returns rads
        angleToRotateDeg = (angleToRotateRad / pi) * 180 #but openscad does rotation in degrees

        fh.write("translate([%f, %f, %f]) {\n" % (xPos, yPos, zPos))
        fh.write("    rotate(v=[%f, %f, %f], a=%f) {\n" % (rotationalAxis[0], rotationalAxis[1], rotationalAxis[2], angleToRotateDeg))
        fh.write("        scale([%f, %f, %f]) {\n" % (1.0, 1.0, aspectRatio))
        fh.write("            sphere(r=%f);\n" % (cell.diameter / 2))
        fh.write("        }\n")
        fh.write("    }\n")
        fh.write("}\n")

    fh.close()

def constructNetworkFromDataFile(filename):
    fh = open(filename, 'r')
    headers = fh.readline()
    line = fh.readline()
    cells = []
    while line != '':
        x,y,z,axial_x,axial_y,axial_z,overlap_amnt,aspect_ratio,length,diameter,generation = line.split(',')
        x = float(x)
        y = float(y)
        z = float(z)
        axial_x = float(axial_x)
        axial_y = float(axial_y)
        axial_z = float(axial_z)
        generation = int(generation)
        pos = vector(x,y,z)
        length = float(length)
        diameter = float(diameter)
        overlap_amnt = float(overlap_amnt)
        # axial_x = 1.*sin(phi)*cos(theta)
        # axial_y = 1.*sin(phi)*sin(theta)
        # axial_z = 1.*cos(phi)
        axis = vector(axial_x,axial_y,axial_z)
        # whoops, didn't include parent cells in the .csv files so reconstructed clusters will have no notion
        # of who is whose parent, will fix if it's ever relevant
        cell = Cell(pos=pos, length=length, diameter=diameter, axis=axis, parent=None, generation=generation)
        cell.overlaps = [overlap_amnt]
        cells.append(cell)
        line = fh.readline()
    fh.close()
    return cells


def constructNetworkFromDataFileOld(filename):
    fh = open(filename, 'r')
    headers = fh.readline()
    line = fh.readline()
    cells = []
    while line != '':
        x,y,z,theta,phi,overlap_amnt,aspect_ratio,length,diameter,generation = line.split(',')
        x = float(x)
        y = float(y)
        z = float(z)
        theta = float(theta)
        phi = float(phi)
        generation = int(generation)
        pos = vector(x,y,z)
        length = float(length)
        diameter = float(diameter)
        overlap_amnt = float(overlap_amnt)
        axial_x = 1.*sin(phi)*cos(theta)
        axial_y = 1.*sin(phi)*sin(theta)
        axial_z = 1.*cos(phi)
        axis = vector(axial_x,axial_y,axial_z)
        # whoops, didn't include parent cells in the .csv files so reconstructed clusters will have no notion
        # of who is whose parent, will fix if it's ever relevant
        cell = Cell(pos=pos, length=length, diameter=diameter, axis=axis, parent=None, generation=generation)
        cell.overlaps = [overlap_amnt]
        cells.append(cell)
        line = fh.readline()
    fh.close()
    return cells


def build_aspect_ratio_distributions(filenames):
    distributions = []
    for filename in filenames:
        fh = open(filename, 'r')
        header = fh.readline()
        line = fh.readline()
        distribution = []
        while line != '':
            distribution.append(float(line))
            line = fh.readline()
        distributions.append(distribution)
        fh.close()
    return distributions


def select_aspect_ratio(distribution):
    return random.choice(distribution)


'''Removes the cells above a certain z coordinate : ceil'''
def removeCellsAbove(ceil, cellList):
    for cel in cellList:
        if cel.pos[2] >= ceil:
            for daughter in cel.children:
                cellList.remove(daughter)
            cellList.remove(cel)


'''Removes the cells below a certain z coordinate : floor'''
def removeCellsBelow(floor, cellList):
    for cel in cellList:
        if cel.pos[2] <= floor:
            for daughter in cel.children:
                cellList.remove(daughter)
            cellList.remove(cel)


def create_cell_stringOld(cell, write_label_string=False):
    if not write_label_string:
        x,y,z = cell.pos
        axial_x, axial_y, axial_z = cell.axis
        phi = acos(axial_z / mag(cell.axis))
        xy_plane_mag = sqrt(axial_x**2.0 + axial_y**2.0)
        theta = asin(axial_y / xy_plane_mag)
        gen_num = cell.generation
        overlap_amnt = sum(cell.overlaps)
        length = float(cell.length)
        diameter = float(cell.diameter)
        aspect_ratio =  length / diameter
        write_label_string = '%f, %f, %f, %f, %f, %f, %f, %f, %f, %d' % (x, y, z, theta, phi, overlap_amnt, aspect_ratio, length, diameter, gen_num)
    else:
        write_label_string="X,Y,Z,THETA,PHI,OVERLAP_AMNT,ASPECT_RATIO,LENGTH,DIAMETER,GENERATION_NUMBER"
    return write_label_string


def output_cell_data_fileOld(cell_list, filename):
    fh = open(filename, 'w')
    # Get the column header names
    cell_string = create_cell_stringOld(None, True)
    fh.write(cell_string)
    fh.write("\n")
    for cell in cell_list:
        cell_string = create_cell_stringOld(cell)
        fh.write(cell_string)
        fh.write('\n')
    fh.close()


def create_cell_string(cell, write_label_string=False):
    if not write_label_string:
        x,y,z = cell.pos
        axial_x, axial_y, axial_z = cell.axis
        # phi = acos(axial_z / mag(cell.axis))
        # xy_plane_mag = sqrt(axial_x**2.0 + axial_y**2.0)
        # theta = asin(axial_y / xy_plane_mag)
        gen_num = cell.generation
        overlap_amnt = sum(cell.overlaps)
        length = float(cell.length)
        diameter = float(cell.diameter)
        aspect_ratio =  length / diameter
        write_label_string = '%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %d' % (x, y, z, axial_x, axial_y, axial_z, overlap_amnt, aspect_ratio, length, diameter, gen_num)
    else:
        write_label_string="X,Y,Z,AXIAL_X,AXIAL_Y,AXIAL_Z,OVERLAP_AMNT,ASPECT_RATIO,LENGTH,DIAMETER,GENERATION_NUMBER"
    return write_label_string


def output_cell_data_file(cell_list, filename):
    fh = open(filename, 'w')
    # Get the column header names
    cell_string = create_cell_string(None, True)
    fh.write(cell_string)
    fh.write("\n")
    for cell in cell_list:
        cell_string = create_cell_string(cell)
        fh.write(cell_string)
        fh.write('\n')
    fh.close()


'''checks if two cells overlap more than permitted by the specified overlapAmnt'''
def overlaps(cellOne, cellTwo, overlapAmnt):

    doesOverlap = False

    if overlapAmnt < 0 or overlapAmnt > 1: #make sure we have a valid overlap parameter
        return None

    for sphereOne in cellOne.sphereMesh:
        for sphereTwo in cellTwo.sphereMesh:
            if mag(sphereOne.pos - sphereTwo.pos) < overlapAmnt*(sphereOne.radius + sphereTwo.radius):
                return True

    for sphereOne in cellOne.sphereMesh:
        for sphereTwo in cellTwo.sphereMesh:
            if mag(sphereOne.pos - sphereTwo.pos) < (sphereOne.radius + sphereTwo.radius):
                overlap = mag(sphereOne.pos - sphereTwo.pos) / (sphereOne.radius + sphereTwo.radius)
                cellOne.overlaps.append(overlap)
                cellTwo.overlaps.append(overlap)

    return False

'''checks overlap for a certain cell against all others in the network'''
def checkOverlap(currCell, cellList, temp, overlapAmnt):

    for cel in cellList + temp:
        if currCell != cel and cel != currCell.parent:
            if overlaps(currCell, cel, overlapAmnt):
                return True
    return False

'''Computes the radius of gyration for the given cell network'''
def computeRadGy(cellList):
    xTot = yTot = zTot = 0 #total sums of x, y, and z coordinates
    for cel in cellList:
        xTot += cel.pos[0]
        yTot += cel.pos[1]
        zTot += cel.pos[2]
    numCells = float(len(cellList)) #number of cells as a float to enable floating point division
    xMean = xTot / numCells #mean x, y and z positions
    yMean = yTot / numCells
    zMean = zTot / numCells

    meanPos = vector(xMean, yMean, zMean) #mean pos vector

    distList = []
    for cel in cellList:
        distList.append((mag(cel.pos - meanPos))**2) #add the magnitude squared of the diff btwn each cell's position and the mean to a list

    return (1.0 / numCells) * sum(distList) #sum the list and multiply by 1/numcells to get the radius of gyration


'''this function takes a vector, an axis (also a vector) and an angle (in radians) by which to rotate the vector about the axis, and returns the rotated vector'''
def rotateVec(vector, axis, theta):

    unitAx = norm(axis) #we want to work with a unit vector for the axis of rotation

    vPar = dot(vector, unitAx)*unitAx #this is the component of v parallel to the axis of rotation, obviously it will not undergo rotation

    vPer = vector - vPar #if we subtract the parallel component of v from v then we should be left with the component of v that is perpendicular to the axis
    #this is the component that will undergo rotation

    #let vPer be a basis vector in the plane of rotation
    #we need one more basis vector for the plane, w

    w = cross(unitAx, vPer)

    vPerRotated = cos(theta)*vPer + sin(theta)*w #the perpendicular component of the vector rotated by theta about r

    vRotated = vPar + vPerRotated #the final rotated vector is just the sum of it's components

    return vRotated

'''Finds the position and axis of a daughter cell given the parent and an angle of attachment'''

def getDaughterPos(cel, theta, length):

    #TODO remove dependency on parent's dimensions for when cells have differing dimensions!!!!

    '''This computes the position of the daughter according to the following reasoning:

    the relationship between the radius of a cross-sectional circle along the ellipsoid and the displacement
    along the major axis of the ellipsoid is given by (x^2) / ((l / 2)^2) + r^2 / R^2 = 1
    where x is the displacement along the axis, r is the radius of the cross-sectional circle, l / 2 is the major axis, and R
    is the radius of the larges cross-sectional circle. Further, x and r are related by tan(theta) = r / x, where theta is, of course,
    the attatchment angle. Combining these two relations yields a solution for axial and radial displacements that satisfyt the attatchment angle.

    The next step is to vectorize these displacements. The axial displacement is along the direction of the parent cell's axis.
    The radial displacement should be a randomly chosen direction perpendicular to the parent's axis. Taking the cross product of the
    parent cell's axis vector with any random vector will yield a result in the plane perpendicular to the axis. So simply generate a vector
    with 3 random components, cross it with the parent's axis, and the resulting vector will be the desired random radial direction'''

    if (len(cel.children) == 0 and cel.generation != 0 and random.random() < 0.80):
        childAxis = norm(cel.axis)

        dispLength = 0.95*((cel.length / 2.0) + (length / 2.0))

        dispVector = cel.pos + dispLength*norm(cel.axis)

        return (dispVector, childAxis)



    else:
        majAxSquared = (cel.length / 2.0)**2                                                #major axis of cell squared

        tanThetSquared = (tan(theta))**2                                                            #tangent of attatchent angle squared

        radSquared = (cel.diameter / 2.0)**2                                                    #the radius of the largest cross-sectional circle squared

        denominator = sqrt((1 / majAxSquared) + (tanThetSquared / radSquared))                      #Computing the axial displacement in steps to reduce nasty syntax

        axialDisplacement = (1 / denominator)*norm(cel.axis)                                     #final step

        height = (axialDisplacement.mag)*tan(theta)                                             #using tan(theta) = r / x to yield r now that x is known

        ranVec = vector(random.uniform(-1,1), random.uniform(-1,1), random.uniform(-1,1))           #generate random vector to cross with axis

        radialDisplacement = cross(ranVec, cel.axis)                                                    #perform cross product

        radialDisplacement.mag = height                                                                     #set the magnitude equal to the radius of the cross-sectional circle at the location of the daughter's end

        relativePos = radialDisplacement + axialDisplacement                                              #the relative position of the end of the daughter cell from the center of the parent

        relativePos.mag = 0.95*(relativePos.mag + (length / 2))                                         #have to add on half a cell length to ensure that this vector points to the center of the daughter

        newPos = cel.pos + relativePos

        return (newPos, relativePos)                                                                 #(position, axis)

'''Incorporates some ranom
dom variance into the angle of attachment'''
def computeVariedTheta(theta, variance):
    #theta = theta +- random(-1,1)*thetaVariance*theta
    newTheta = theta + random.uniform(-1,1)*variance*theta
    return newTheta

'''Sets all objects to be invisible and removes all references to them to free them for garbage collection'''
def clearScene(visualScene): #removes all of the objects in the scene from the main memory storage that Vpython keeps them in
    for obj in visualScene.objects: #so that a memory leak isn't triggered
        obj.visible = False
        del obj
