from classes import Menu
from classes.Slot import OvalSlot
from classes.Pattern import Pattern


if __name__ == '__main__':

    # for testing all dimensions are predefined
    ovalSlot = OvalSlot(length=10, radius=4)
    metalSheet = Pattern(length=120, height=20, slot=ovalSlot, minSpace=2)

    MenuInit = Menu.Menu(slot=ovalSlot, pattern=metalSheet)

    while True:
        MenuInit()
