from visual import *
from math import *

__author__ = "Elyes Graba"
__credits__ = ["Peter Yunker", "Shane Jacobeen"]
__version__ = "3.0.1"
__maintainer__ = "Elyes Graba"
__email__ = "elyesgraba@gatech.edu"
__status__ = "Development"

class Cell(object):

    '''constructor'''
    def __init__(self, pos, length, diameter, axis, parent, generation):
        self.pos = pos
        self.length = length
        self.diameter = diameter
        self.axis = axis
        self.parent = parent
        self.generation = generation
        self.graphical = None
        self.children = []
        self.sphereMesh = []
        self.fillSpheres()
        self.createGraphic(generation)
        self.overlaps = []
        self.failedSpawns = 0

    '''creates the visual object to represent the cell'''
    def createGraphic(self, generation):
        self.graphical = ellipsoid(pos = self.pos, axis = self.axis, length = self.length, width = self.diameter, height = self.diameter, color = color.hsv_to_rgb(((1.0 / 15.0)*generation, .5, .75)))

        '''
        this is the original fillSpheres() method, but its being retired for its incorrect placement of overlap spheres
        when dealing with cells that have certain dimensions. Rather than always placing spheres proportionally according to the
        aspect ratio of the cell in question, this method seems to sometimes place spheres differently (even relatively speaking)
        for two cells of the same aspect ratio but of different physical dimensions. For example, for a cell of length 10 and diameter 5
        this method might place spheres correctly, but for a cell of length 4 and diameter 2, this method may erroneuously place spheres
        outside of the bounds of the cell itself for that reason this version of the method is being retired, but kept in this file as a comment
        in case its functionality ever needs to be remembered
        '''

    '''def fillSpheres(self):
        centerSphere = Sphere(self.pos, self.diameter / 2)
        centerSphere.graphical = sphere(pos = centerSphere.pos, radius = centerSphere.radius, color = color.green)
        frontBackRad = (math.sqrt(3) / 2) * (self.diameter / 2)
        frontSphere = Sphere(self.pos + ((self.length - self.diameter) / (self.diameter / 2))*norm(self.axis), frontBackRad)
        frontSphere.graphical = sphere(pos = frontSphere.pos, radius = frontSphere.radius, color = color.green)
        backSphere = Sphere(self.pos - ((self.length - self.diameter) / (self.diameter / 2))*norm(self.axis), frontBackRad)
        backSphere.graphical = sphere(pos = backSphere.pos, radius = backSphere.radius, color = color.green)
        self.sphereMesh.append(centerSphere)
        self.sphereMesh.append(backSphere)
        self.sphereMesh.append(frontSphere)'''

    '''this is the new fillSpheres method'''

    def fillSpheres(self):
        #Not Creating graphical objects for the spheres because it wastes time and memory, they don't need to be seen
        centerSphere = Sphere(self.pos, self.diameter / 2) #place a sphere at the center of the cell with radius equal to the largest cross-sectional circle of the cell
        #centerSphere.graphical = sphere(pos=centerSphere.pos, radius=centerSphere.radius, color=color.green)
        fociDistance = ((self.length / 2)**2 - (self.diameter / 2)**2)**0.5 #calculate the distance from the center of the cell to its foci
        fociOnePos = self.pos + fociDistance*norm(self.axis) #obtain positions of both foci
        fociTwoPos = self.pos - fociDistance*norm(self.axis)
        fociRadii = (self.length / 2) - fociDistance #radius of focal spheres is remaining distance from foci to vertex of ellipsoid
        fociOne = Sphere(fociOnePos, fociRadii) #the two focal sphere objects themselves
        fociTwo = Sphere(fociTwoPos, fociRadii)
        #fociOne.graphical=sphere(pos=fociOne.pos, radius=fociOne.radius, color=color.green) #create graphicals for the spheres
        #fociTwo.graphical=sphere(pos=fociTwo.pos, radius=fociTwo.radius, color=color.green)
        middleDistance = fociDistance / 2 #place additional spheres halfway between focal spheres and centersphere
        middleRadius = ((1 - (middleDistance / (self.length / 2))**2)**0.5) * (self.diameter / 2) #calculate an appropriate radius for the spheres according to the equation for an ellipsoid
        middleOnePos = self.pos + middleDistance*norm(self.axis)
        middleTwoPos = self.pos - middleDistance*norm(self.axis)
        middleOne = Sphere(middleOnePos, middleRadius)
        middleTwo = Sphere(middleTwoPos, middleRadius)
        #middleOne.graphical = sphere(pos=middleOne.pos, radius=middleOne.radius, color=color.blue)
        #middleTwo.graphical = sphere(pos=middleTwo.pos, radius=middleTwo.radius, color=color.blue)
        self.sphereMesh = [middleOne, middleTwo, centerSphere, fociOne, fociTwo]


class RootCell(Cell):
    def __init__(self, pos, length, diameter, axis, parent, generation):
        super(self.__class__, self).__init__(pos, length, diameter, axis, parent, generation)

    def switchGrowthDirection(self):
        self.axis = - self.axis

class Sphere(object):

    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
        self.graphical = None
