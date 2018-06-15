from itertools import groupby
import random
from pprint import pprint

class Location():
    def __init__(self, left, right, up, down):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
    
    def __str__(self):
        return "(l: {left}, r: {right}, u:{up}, d:{down})".format(
            left = self.left, right = self.right, up = self.up, down = self.down)
    
    def __repr__(self):
        return str(self)

_list = [
    Location(left = 0,  right = 10, up = 0,     down = 20),
    # Location(left = 11, right = 20, up = 0,     down = 20),
    Location(left = 21, right = 30, up = 0,     down = 20),
    Location(left = 31, right = 40, up = 0,     down = 20),
    # Location(left = 0,  right = 10, up = 21,    down = 40),
    Location(left = 11, right = 20, up = 21,    down = 40),
    Location(left = 21, right = 30, up = 21,    down = 40),
    Location(left = 31, right = 40, up = 21,    down = 40),
    # Location(left = 0,  right = 10, up = 41,    down = 60),
    Location(left = 11, right = 20, up = 41,    down = 60),
    Location(left = 21, right = 30, up = 41,    down = 60),
    Location(left = 31, right = 40, up = 41,    down = 60),
    Location(left = 0,  right = 10, up = 61,    down = 80),
    # Location(left = 11, right = 20, up = 61,    down = 80),
    Location(left = 21, right = 30, up = 61,    down = 80),
    # Location(left = 31, right = 40, up = 61,    down = 80),
    Location(left = 0,  right = 10, up = 81,    down = 100),
    # Location(left = 11, right = 20, up = 81,    down = 100),
    Location(left = 21, right = 30, up = 81,    down = 100),
    Location(left = 31, right = 40, up = 81,    down = 100)]

pprint(_list)
_unsortedList = random.sample(_list, len(_list))
pprint(_unsortedList)

def GetMatrixLineUpDownColumnLeftRight(unsortedList):
    sortedListByUpLeft = sorted(unsortedList, key = lambda location: (location.up, location.left))
    pprint(sortedListByUpLeft)
    matrixSorted = [
        (
            up, down,
            [location for location in listIterator])
        for (up, down), listIterator in groupby(sortedListByUpLeft, lambda location: (location.up, location.down))]
    pprint(matrixSorted)
    return matrixSorted

def GetMatrixLineLeftRightColumnUpDown(unsortedList):
    sortedListByLRUD = sorted(unsortedList, key = lambda location: (location.left, location.right, location.up, location.down))
    pprint(sortedListByLRUD)
    matrixSorted = [
        (
            left, right,
            [location for location in listIterator])
        for (left, right), listIterator in groupby(sortedListByLRUD, lambda location: (location.left, location.right))]
    pprint(matrixSorted)
    return matrixSorted

matrixLineUpDownColumnLeftRight = GetMatrixLineUpDownColumnLeftRight(_unsortedList)

closedList = []
for up, down, line in matrixLineUpDownColumnLeftRight:
    processingItem = line[0]
    for location in line[1:]:
        if(processingItem.right + 1 == location.left):
            processingItem.right = location.right
        else:
            closedList.append(processingItem)
            processingItem = location
    closedList.append(processingItem)

matrixLineLeftRightColumnUpDown = GetMatrixLineLeftRightColumnUpDown(closedList)

closedList = []
for left, right, line in matrixLineLeftRightColumnUpDown:
    processingItem = line[0]
    for location in line[1:]:
        if(processingItem.down + 1 == location.up):
            processingItem.down = location.down
        else:
            closedList.append(processingItem)
            processingItem = location
    closedList.append(processingItem)

pprint(closedList)



