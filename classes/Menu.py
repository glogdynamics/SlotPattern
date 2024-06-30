import matplotlib.pyplot as plt
from classes.slotPattern import Slot, Pattern
import ezdxf


class Menu:

    def __init__(self,
                 slot: Slot,
                 pattern: Pattern):

        self.slot = slot
        self.pattern = pattern
        self.pattern.slot = self.slot
        self.patternGenerator = None

    def __call__(self, *args, **kwargs):
        print("You are in main menu")
        print("Press c to configure pattern")
        print("Press p to plot generated scheme")
        print("Press s to save pattern to CAD")
        print("Press q to quit\n")

        userInput = input("User input:\n").lower()

        if userInput == "c": self.configurePattern()
        elif userInput == "p": self.plotPattern()
        elif userInput == "s": self.savePattern()
        elif userInput == "q": exit()
        else: return

    def configurePattern(self):
        print("Configure slot\n")
        len = float(input("Give slot length:\n"))
        rad = float(input("Give slot radius:\n"))
        self.slot.length = len
        self.slot.radius = rad
        print(f"Your slot has {self.slot.length} length and {self.slot.radius} radius")

        print("Configure Pattern\n")
        sheetLen = float(input("Give metal sheet length:\n"))
        sheetHeight = float(input("Give metal sheet heights:\n"))
        minSpacing = float(input("Give mminimum spacing between slots:\n"))
        self.pattern.length = sheetLen
        self.pattern.height = sheetHeight
        self.pattern.minSpace = minSpacing
        self.pattern.slot = self.slot

        print(f"Your pattern is {self.pattern.length} x {self.pattern.height}")

    def plotPattern(self):
        fig, ax = plt.subplots()
        for origin in range(len(self.pattern.distributionAlongLength)):
            x, y = self.pattern.slotCorners(slotCounter=origin)
            ax.plot(x, y)
        plt.show()

    def savePattern(self):

        file_name = "Test.dxf"

        # Tworzenie nowego dokumentu DXF
        doc = ezdxf.new(dxfversion='R2010')

        # Dodanie warstwy do dokumentu
        doc.layers.add(name='MyLayer', color=7)  # Kolor biały

        # Uzyskanie modelspace, aby dodać do niego elementy
        msp = doc.modelspace()

        # Add main dimensions
        msp.add_line(start=(0, 0), end=(0, -self.pattern.height))
        msp.add_line(start=(0, 0), end=(self.pattern.length, 0))
        msp.add_line(start=(self.pattern.length, 0), end=(self.pattern.length, -self.pattern.height))
        msp.add_line(start=(0, -self.pattern.height), end=(self.pattern.length, -self.pattern.height))

        for origin in range(len(self.pattern.distributionAlongLength)):
            x, y = self.pattern.slotCorners(slotCounter=origin)

            msp.add_line((x[5], y[5]), (x[0], y[0]), dxfattribs={'layer': 'MyLayer'})
            msp.add_line((x[2], y[2]), (x[3], y[3]), dxfattribs={'layer': 'MyLayer'})

            arc_center1 = (x[2], y[1])
            arc_center2 = (x[3], y[4])

            msp.add_arc(center=arc_center1, radius=self.slot.radius, start_angle=90, end_angle=-90)
            msp.add_arc(center=arc_center2, radius=self.slot.radius, start_angle=-90, end_angle=90)


        # Zapisanie pliku DXF
        doc.saveas(file_name)
        print(f'Plik DXF zapisany jako {file_name}')




