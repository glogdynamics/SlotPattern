from abc import ABCMeta, abstractmethod, abstractproperty
from classes.Objects import Arc, Line, Point
from classes.Objects import PlotterPrepare, Transform


class Slot(metaclass=ABCMeta):

    @property
    @abstractmethod
    def length(self):
        pass

    @property
    @abstractmethod
    def width(self):
        pass


class OvalSlot(Slot):

    def __init__(self,
                 length: float = 0,
                 radius: float = 0):

        # Basics
        self._length = length
        self.radius = radius

        # Properties
        self.arc1 = Arc(radius=self.radius, center=Point(self.radius, 0),
                        startAngle=90, endAngle=270)

        self.arc2 = Arc(radius=self.radius, center=Point(self.length - self.radius, 0),
                        startAngle=-90, endAngle=90)

        self.line1 = Line(startPoint=Point(self.radius, self.radius),
                          endPoint=Point(self.length - self.radius, self.radius))

        self.line2 = Line(startPoint=Point(self.radius, -self.radius),
                          endPoint=Point(self.length - self.radius, -self.radius))

    # PROPERTIES

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, val):
        self._length = val

    @property
    def width(self):
        return 2*self.radius


class SlotTransform:

    @staticmethod
    def setOffset(baseObject: Slot, offsetX: float = 0, offsetY: float = 0):
        """Get all attributes that are point type.
        Tranzlate them by given values

        """
        for attr in dir(baseObject):
            obj2d = getattr(baseObject, attr)
            if (type(obj2d) is Arc) or (type(obj2d) is Line):
                Transform.setOffset(obj2d, offsetX, offsetY)


class SlotPlotter:

    @staticmethod
    def ovalSlot2collection(obj: Slot) -> object:

        collection = []
        for propName in dir(obj):
            prop = getattr(obj, propName)
            if type(prop) is Line or type(prop) is Arc:
                collection.append(PlotterPrepare.convert2patch(prop))

        return PlotterPrepare.makeCollection(collection)


# Testing
if __name__ == "__main__":

    aa = OvalSlot(length=15, radius=2)
    # arc1 = Arc(center=Point(0, 0), radius=2)
    #
    # print(arc1.center())
    # Transform.setOffset(arc1, 10, 10)
    # print(arc1.center())

    # print(aa.arc1.startPoint(), aa.arc1.center())
    # Transform.setOffset(aa.arc1, 10, 10)
    # print(aa.arc1.startPoint(), aa.arc1.center())

    SlotTransform.setOffset(aa, offsetX=5, offsetY=10)

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    ax.add_collection(SlotPlotter.ovalSlot2collection(aa))

    plt.show()
