from classes import Menu
from classes import slotPattern


if __name__ == '__main__':

    # for testing all dimensions are predefined
    ovalSlot = slotPattern.Slot(length=50, radius=4)
    metalSheet = slotPattern.Pattern(length=120, height=20, slot=ovalSlot, minSpace=0)

    MenuInit = Menu.Menu(slot=ovalSlot, pattern=metalSheet)

    while True:
        MenuInit()
