from math import sin, cos, radians
from abc import ABC, abstractmethod, abstractproperty
# from matplotlib.patches import Arc as ptchArc
# from matplotlib.patches import Polygon as ptchPoly
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection


class Object2D(ABC):
    pass

    # @abstractmethod
    # def getAsPatch(self):
    #     raise NotImplemented


class Point:

    def __init__(self,
                 posX: float = 0,
                 posY: float = 0
                 ) -> None:

        self.posX = posX
        self.posY = posY

    def __call__(self):
        return tuple([self.posX, self.posY])


class Line(Object2D):
    """
    Generic object that allow to initialize Line
    """

    def __init__(self,
                 startPoint: Point = None,
                 endPoint: Point = None
                 ):

        self.startPoint = startPoint
        self.endPoint = endPoint

    # Methods

    # def getAsPatch(self) -> ptchPoly:
    #     """Returns two-point polygon from matplotlib.patches lib
    #
    #     """
    #     return ptchPoly([(self.startPoint.posX, self.startPoint.posY), (self.endPoint.posX, self.endPoint.posY)],
    #                     closed=False, fill=False, linewidth=1)


class Rectangle(Object2D):

    def __init__(self,
                 length: float,
                 height: float
                 ) -> None:

        self.length = length
        self.height = height
        # self.corners = [Line(Point(0, 0), Point(self.length, 0)),
        #                 Line(Point(self.length, 0), Point(self.length, self.height)),
        #                 Line(Point(self.length, self.height), Point(0, self.height)),
        #                 Line(Point(0, self.height), Point(0, 0))]

        self.corners = [(0, 0), (self.length, 0), (self.length, self.height), (0, self.height)]


class Arc(Object2D):
    """
    Generic object that allow to initialize Arc
    """

    def __init__(self,
                 radius: float,
                 center: Point = None,
                 startAngle: float = 0,
                 endAngle: float = 180
                 ):

        self.radius = radius
        self.center = center
        self.startAngle = startAngle
        self.endAngle = endAngle

        self.startPoint: Point = Point(posX=(self.radius+self.center.posX)*cos(radians(self.startAngle)),
                                       posY=(self.radius+self.center.posY)*sin(radians(self.startAngle)))
        self._midAngle: float = (self.startAngle + self.endAngle)/2
        self.midPoint: Point = Point(posX=(self.radius+self.center.posX)*cos(radians(self._midAngle)),
                                     posY=(self.radius+self.center.posY)*sin(radians(self._midAngle)))
        self.endPoint: Point = Point(posX=(self.radius+self.center.posX)*cos(radians(self.endAngle)),
                                     posY=(self.radius+self.center.posY)*sin(radians(self.endAngle)))

    # Methods

    # def getAsPatch(self) -> ptchArc:
    #     """Return matplotlib object for plotting
    #
    #     """
    #     return ptchArc(xy=self.center,
    #                    width=self.radius, height=self.radius,
    #                    theta1=self.startAngle, theta2=self.endAngle)


class Transform:

    @staticmethod
    def backPoints2origin(baseObject: Object2D):
        """Restores all points from object to (0,0) position

        """
        for attr in dir(baseObject):
            obj = getattr(baseObject, attr)
            if type(obj) is Point:
                obj.posX = 0
                obj.posY = 0

    @staticmethod
    def setOffset(baseObject: Object2D, offsetX: float = 0, offsetY: float = 0):
        """Get all attributes that are point type.
        Tranzlate them by given values

        """
        for attr in dir(baseObject):
            obj = getattr(baseObject, attr)
            if type(obj) is Point:
                obj.posX += offsetX
                obj.posY += offsetY


class PlotterPrepare:

    @staticmethod
    def recognizeObject(baseObject: Object2D) -> str:
        """Function makes to recognize type of object

        """
        if type(baseObject) is Line:
            return "line"

        elif type(baseObject) is Arc:
            return "arc"

        elif type(baseObject) is Rectangle:
            return "rectangle"

        else:
            return ""

    @staticmethod
    def line2line(baseObject: Line) -> patches:
        """Converts base Line object into Matplotlib.Patches Polygon (with 2 points)
        Used for plotting lines.

        """
        return patches.Polygon(xy=[baseObject.startPoint(), baseObject.endPoint()],
                               closed=False,
                               fill=False,
                               linewidth=1)

    @staticmethod
    def arc2arc(baseObject: Arc):
        """Converts base Arc object into Matplotlib.Patches Arc
        Used for plotting lines.

        """
        return patches.Arc(xy=(baseObject.center.posX, baseObject.center.posY),
                           width=baseObject.radius*2, height=baseObject.radius*2,
                           theta1=baseObject.startAngle, theta2=baseObject.endAngle)

    @staticmethod
    def rect2rect(baseObject: Rectangle):

        return patches.Polygon(xy=baseObject.corners, fill=False, linewidth=1)

    @staticmethod
    def convert2patch(baseObject: Object2D):
        recognizedType = PlotterPrepare.recognizeObject(baseObject)

        if recognizedType == "line":
            return PlotterPrepare.line2line(baseObject)

        elif recognizedType == "arc":
            return PlotterPrepare.arc2arc(baseObject)

        elif recognizedType == "rectangle":
            return PlotterPrepare.rect2rect(baseObject)

    @staticmethod
    def makeCollection(patchesList: list):
        """Returns collection that can be plotted directly

        """
        return PatchCollection(patches=patchesList, match_original=True)


if __name__ == "__main__":

    line1 = Line(startPoint=Point(0, 0), endPoint=Point(1, 1))
    arc1 = Arc(center=Point(0, 0), radius=1)

    Transform.setOffset(baseObject=line1, offsetX=10, offsetY=10)
    print(line1.startPoint())
    print(line1.endPoint())

    line1.startPoint = Point()
    print(line1.startPoint())

    import matplotlib.pyplot as plt

    plt.figure()
    ax = plt.gca()
    obj1 = PlotterPrepare.convert2patch(line1)
    ax.add_patch(obj1)

    Transform.setOffset(arc1, 5, 5)

    obj2 = PlotterPrepare.convert2patch(arc1)
    ax.add_patch(obj2)

    print(arc1.startPoint())
    print(arc1.endPoint())
    plt.show()

    #
    #
    # luk1 = Arc(radius=1, center=(0, 0), startAngle=0, endAngle=360)
    # linia1 = Line(startPoint=(0, 0), endPoint=(1, 1))
    #
    #
    # plt.figure()
    #
    # ax = plt.gca()
    # ax.add_patch(luk1.getAsPatch())
    # ax.add_patch(linia1.getAsPatch())
    # ax.set_xlim([-1, 1])
    # ax.set_ylim([-1, 1])
    # plt.show()


