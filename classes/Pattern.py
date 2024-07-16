from classes.Slot import Slot, OvalSlot
from classes.Objects import Rectangle
from classes.Distribution import Distribution


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
        self.domain = Rectangle(self.length, self.height)

        # optional
        self.minSpace = minSpace

        # Properties
        self.originsX = Distribution(holeLength=self.slot.length, domainLength=self.length, minSpacing=self.minSpace).origins
        self.originsY = Distribution(holeLength=self.slot.width, domainLength=self.height, minSpacing=self.minSpace).origins

    # PROPERTIES
    @property
    def origins(self) -> list:
        origins = []
        for column in self.originsX:
            for row in self.originsY:
                origins.append([column, row])
        return origins


if __name__ == "__main__":

    ovalHole = OvalSlot(length=10, radius=2)
    metalSheet = Pattern(length=120, height=100, slot=ovalHole)

    print(metalSheet.originsX)
