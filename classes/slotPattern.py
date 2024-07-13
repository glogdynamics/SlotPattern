import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from classes.Objects import Arc, Line


class Slot:

    def __init__(self,
                 length: float = 0,
                 radius: float = 0):

        # Basics
        self.length = length
        self.radius = radius
        self.width = 2*self.radius

        # Manipulators
        self.offsetX: float = 0
        self.offsetY: float = 0

    # PROPERTIES

    @property
    def arc1(self) -> Arc:
        return Arc(radius=self.radius, center=(self.radius + self.offsetX, 0 + self.offsetY),
                   startAngle=90, endAngle=270)

    @property
    def arc2(self) -> Arc:
        return Arc(radius=self.radius, center=(self.length - self.radius + self.offsetX, 0 + self.offsetY),
                   startAngle=-90, endAngle=90)

    @property
    def line1(self) -> Line:
        return Line(startPoint=(self.radius + self.offsetX, self.radius/2 + self.offsetY),
                    endPoint=(self.length - self.radius + self.offsetX, self.radius/2 + self.offsetY))

    @property
    def line2(self) -> Line:
        return Line(startPoint=(self.radius + self.offsetX, -self.radius/2 + self.offsetY),
                    endPoint=(self.length - self.radius + self.offsetX, -self.radius/2 + self.offsetY))

    def getPatchCollector(self):
        collection = []
        collection += [self.arc1.getAsPatch(),
                       self.line1.getAsPatch(),
                       self.arc2.getAsPatch(),
                       self.line2.getAsPatch()]

        p = PatchCollection(patches=collection, match_original=True)

        return p

    # METHODS

    def offsetSlot(self, xOffset: float = 0, yOffset: float = 0):
        self.offsetX = xOffset
        self.offsetY = yOffset

    def rotateSlot(self, angle: float = 0):
        pass

    def scaleSlot(self, scaleLength: float = 1, scaleWidth: float = 1):
        pass


class Pattern:

    def __init__(self,
                 length: float = 0,
                 height: float = 0,
                 slot: Slot = None,
                 minSpace: float = 0):

        # must have
        self.length = length
        self.height = height
        self.slot = slot

        # optional
        self.minSpace = minSpace

    # distribution fcns

    @property
    def slotsAlongLength(self) -> int:
        return Pattern.maxEntities(self.length, self.slot.length, self.minSpace)

    @property
    def slotsAlongHeight(self) -> int:
        return Pattern.maxEntities(self.height, self.slot.width, self.minSpace)

    @property
    def gapsAlongLength(self) -> float:
        return Pattern.slotsDistance(self.length, self.slot.length, self.minSpace)

    @property
    def gapsAlongHeight(self) -> float:
        return Pattern.slotsDistance(self.height, self.slot.width, self.minSpace)

    @property
    def distributionAlongLength(self):
        positions = []
        for i in range(0, self.slotsAlongLength):
            positions.append(self.gapsAlongLength+self.slot.length*i+self.gapsAlongLength*i)
        return positions

    @property
    def distributionAlongHeight(self):
        positions = []
        for i in range(0, self.slotsAlongHeight):
            positions.append(self.gapsAlongHeight+self.slot.width/2+self.slot.width*i+self.gapsAlongHeight*i)
        return positions

    @property
    def origins(self) -> list:
        origins = []
        for column in self.distributionAlongLength:
            for row in self.distributionAlongHeight:
                origins.append([column, row])
        return origins

    @property
    def originsX(self) -> list:
        return [pos[0] for pos in self.origins]

    @property
    def originsY(self) -> list:
        return [pos[1] for pos in self.origins]

    @property
    def amountOfOrigins(self) -> int:
        return len(self.origins)

    @staticmethod
    def maxEntities(dimension: float, slotLength: float, minSpacing: float = 0) -> int:
        """Allows to calculate max number of slots in given dimension

        """
        entities = 0
        if slotLength >= dimension:
            print("Slot cant be longer than main dimension!")
            return entities

        elif (dimension < 0) or (slotLength < 0):
            print("All dimensions must be greater than zero!")
            return entities

        else:
            entities = np.floor((dimension-minSpacing)/(slotLength+minSpacing))

            # Number of slots cant be equal to distance
            if dimension == entities*slotLength:
                entities = entities - 1

            return int(entities)

    @staticmethod
    def slotsDistance(dimension: float, slotLength: float, minSpacing: float = 0) -> float:
        entities = Pattern.maxEntities(dimension, slotLength, minSpacing)
        freeSpace = dimension - (entities*slotLength)
        betweenSpace = freeSpace/(entities+1)
        return betweenSpace

    def getBoundaryAsPatch(self):
        boundary = Polygon(xy=[(0, 0), (self.length, 0), (self.length, self.height), (0, self.height)],
                           fill=False, linewidth=1)
        return boundary


if __name__ == "__main__":

    """Only for testing
    """

    fasola = Slot(length=20, radius=4)
    blacha = Pattern(length=60, height=20, slot=fasola, minSpace=0)

    print(blacha.origins)

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    #ax.scatter(blacha.originsX, blacha.originsY)
    ax.add_collection(fasola.getPatchCollector())

    plt.show()
