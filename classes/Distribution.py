import numpy as np


class Distribution:

    def __init__(self,
                 holeLength: float,
                 domainLength: float,
                 minSpacing: float = 0
                 ) -> None:

        self.holeLength = holeLength
        self.domainLength = domainLength
        self.minSpacing = minSpacing

    # Properties

    @property
    def maxEntities(self) -> int:
        """Allows to calculate max number of slots

        """
        entities = 0
        if self.holeLength >= self.domainLength:
            print("Slot cant be longer than main dimension!")
            return entities

        elif (self.domainLength < 0) or (self.holeLength < 0):
            print("All dimensions must be greater than zero!")
            return entities

        else:
            entities = np.floor((self.domainLength - self.minSpacing) / (self.holeLength + self.minSpacing))

            # Number of slots cant be equal to distance
            if self.domainLength == entities * self.holeLength:
                entities = entities - 1

            return int(entities)

    @property
    def distanceBetweenHoles(self) -> float:
        """Represents distance between holes

        """
        freeSpace = self.domainLength - (self.maxEntities*self.holeLength)
        betweenSpace = freeSpace/(self.maxEntities+1)
        return betweenSpace

    @property
    def origins(self) -> list:
        """Represents positions of origins along domain

        """
        positions = []
        for i in range(0, self.maxEntities):
            positions.append(self.distanceBetweenHoles+self.holeLength*i+self.distanceBetweenHoles*i)
        return positions


if __name__ == "__main__":

    domain1 = Distribution(holeLength=20, domainLength=100, minSpacing=10)

    print(domain1.origins)

