from math import sin, cos, radians
from matplotlib.patches import Arc as ptchArc
from matplotlib.patches import Polygon as ptchPoly


class Line:
    """
    Generic object that allow to initialize Line
    """

    def __init__(self,
                 startPoint: tuple = None,
                 endPoint: tuple = None
                 ):

        self.startPoint = startPoint
        self.endPoint = endPoint

    # Methods

    def getAsPatch(self) -> ptchPoly:
        """Returns two-point polygon from matplotlib.patches lib

        """
        return ptchPoly([self.startPoint, self.endPoint], closed=False, fill=False, linewidth=1)


class Arc:
    """
    Generic object that allow to initialize Arc
    """

    def __init__(self,
                 radius: float,
                 center: tuple = (0, 0),
                 startAngle: float = 0,
                 endAngle: float = 180
                 ):

        self.radius = radius
        self.center = center
        self.startAngle = startAngle
        self.endAngle = endAngle

        self.startPoint: tuple = (self.radius*cos(radians(self.startAngle)), self.radius*sin(radians(self.startAngle)))
        self._midAngle: float = (self.startAngle + self.endAngle)/2
        self.midPoint: tuple = (self.radius*cos(radians(self._midAngle)), self.radius*sin(radians(self._midAngle)))
        self.endPoint: tuple = (self.radius*cos(radians(self.endAngle)), self.radius*sin(radians(self.endAngle)))

    # Methods

    def getAsPatch(self) -> ptchArc:
        """Return matplotlib object for plotting

        """
        return ptchArc(xy=self.center,
                       width=self.radius, height=self.radius,
                       theta1=self.startAngle, theta2=self.endAngle)


if __name__ == "__main__":

    import matplotlib.pyplot as plt



    luk1 = Arc(radius=1, center=(0, 0), startAngle=0, endAngle=360)
    linia1 = Line(startPoint=(0, 0), endPoint=(1, 1))


    plt.figure()

    ax = plt.gca()
    ax.add_patch(luk1.getAsPatch())
    ax.add_patch(linia1.getAsPatch())
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    plt.show()


