import numpy as np


class Slot:

    def __init__(self,
                 length: float = 0,
                 radius: float = 0):

        self.length = length
        self.radius = radius
        self.width = 2*self.radius

    @property
    def slotEnd1(self) -> list:
        points = [[self.radius, -self.radius], [0, 0], [self.radius, self.radius]]
        return points

    @property
    def slotEnd2(self) -> list:
        points = [[self.length - self.radius, -self.radius], [self.length, 0], [self.length - self.radius, self.radius]]
        return points

    @property
    def cornerPoints(self) -> list:
        corners = []
        corners.extend(self.slotEnd1)
        corners.extend([x for x in self.slotEnd2[::-1]])
        #corners.extend(self.slotEnd2)
        cornersX = [point[0] for point in corners]
        cornersY = [point[1] for point in corners]
        return [cornersX, cornersY]


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
    def gapsAlongLength(self) -> float:
        return Pattern.slotsDistance(self.length, self.slot.length, self.minSpace)

    @property
    def distributionAlongLength(self):
        positions = []
        for i in range(0, self.slotsAlongLength):
            positions.append(self.gapsAlongLength+self.slot.length*i+self.gapsAlongLength*i)
        return positions

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

    # plotting fcns

    def slotCorners(self, slotCounter: int):
        offset = self.distributionAlongLength[slotCounter]
        x, y = self.slot.cornerPoints
        y = [coordY-self.height/2 for coordY in y]
        points = [Pattern.offsetEntity(coordX, offset) for coordX in x]
        return [points, y]

    @staticmethod
    def offsetEntity(basePosition: float, offset: float):
        finalPosition = basePosition + offset
        return finalPosition


if __name__ == "__main__":

    fasola = Slot(length=100, radius=4)
    blacha = Pattern(length=600, height=300, slot=fasola, minSpace=30)

    print(blacha.distributionAlongLength)

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.plot(x, y)

    for origin in range(len(blacha.distributionAlongLength)):
        x, y = blacha.slotCorners(slotCounter=origin)
        ax.plot(x, y)

    plt.show()
