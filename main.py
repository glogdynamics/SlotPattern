# This is a sample Python script.
from classes import Menu
from classes import slotPattern

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # for testing all dimensions are predefined
    fasola = slotPattern.Slot(40, 4)
    blacha = slotPattern.Pattern(600, 40, fasola, 30)

    MenuInit = Menu.Menu(slot=fasola, pattern=blacha)

    while True:
        MenuInit()
