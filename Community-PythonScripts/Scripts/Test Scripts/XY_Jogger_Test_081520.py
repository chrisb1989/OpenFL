# -*- coding: utf-8 -*-

from Tkinter import *
from OpenFL import Printer, FLP
import copy
import numpy as np


p=Printer.DummyPrinter() #change to Printer.Printer before using
root = Tk()
root.title('XY Calibration Tool')
gridCal = np.ravel(p.read_grid_table())
test = IntVar()
test.set("1")

gridPos = IntVar()
gridPos.set("1")

def backMove():
	print gridMap[gridPos]

def leftMove():
	print gridMap[gridPos]

def rightMove():
	print gridMap[gridPos]

def forwardMove():
	print (gridMap[gridPos])

# define buttons

Label01 = Label (root, text=str(gridCal[0][0][0]) + " , " + str(gridCal[0][0][1]), height = 5, width = 12, relief = "raised")
Label02 = Label (root, text=str(gridCal[0][1][0]) + " , " + str(gridCal[0][1][1]), height = 5, width = 12, relief = "raised")
Label03 = Label (root, text=str(gridCal[0][2][0]) + " , " + str(gridCal[0][2][1]), height = 5, width = 12, relief = "raised")
Label04 = Label (root, text=str(gridCal[0][3][0]) + " , " + str(gridCal[0][3][1]), height = 5, width = 12, relief = "raised")
Label05 = Label (root, text=str(gridCal[0][4][0]) + " , " + str(gridCal[0][4][1]), height = 5, width = 12, relief = "raised")
Label06 = Label (root, text=str(gridCal[1][0][0]) + " , " + str(gridCal[1][0][1]), height = 5, width = 12, relief = "raised")
Label07 = Label (root, text=str(gridCal[1][1][0]) + " , " + str(gridCal[1][1][1]), height = 5, width = 12, relief = "raised")
Label08 = Label (root, text=str(gridCal[1][2][0]) + " , " + str(gridCal[1][2][1]), height = 5, width = 12, relief = "raised")
Label09 = Label (root, text=str(gridCal[1][3][0]) + " , " + str(gridCal[1][3][1]), height = 5, width = 12, relief = "raised")
Label10 = Label (root, text=str(gridCal[1][4][0]) + " , " + str(gridCal[1][4][1]), height = 5, width = 12, relief = "raised")
Label11 = Label (root, text=str(gridCal[2][0][0]) + " , " + str(gridCal[2][0][1]), height = 5, width = 12, relief = "raised")
Label12 = Label (root, text=str(gridCal[2][1][0]) + " , " + str(gridCal[2][1][1]), height = 5, width = 12, relief = "raised")
Label13 = Label (root, text=str(gridCal[2][2][0]) + " , " + str(gridCal[2][2][1]), height = 5, width = 12, relief = "raised")
Label14 = Label (root, text=str(gridCal[2][3][0]) + " , " + str(gridCal[2][3][1]), height = 5, width = 12, relief = "raised")
Label15 = Label (root, text=str(gridCal[2][4][0]) + " , " + str(gridCal[2][4][1]), height = 5, width = 12, relief = "raised")
Label16 = Label (root, text=str(gridCal[3][0][0]) + " , " + str(gridCal[3][0][1]), height = 5, width = 12, relief = "raised")
Label17 = Label (root, text=str(gridCal[3][1][0]) + " , " + str(gridCal[3][1][1]), height = 5, width = 12, relief = "raised")
Label18 = Label (root, text=str(gridCal[3][2][0]) + " , " + str(gridCal[3][2][1]), height = 5, width = 12, relief = "raised")
Label19 = Label (root, text=str(gridCal[3][3][0]) + " , " + str(gridCal[3][3][1]), height = 5, width = 12, relief = "raised")
Label20 = Label (root, text=str(gridCal[3][4][0]) + " , " + str(gridCal[3][4][1]), height = 5, width = 12, relief = "raised")
Label21 = Label (root, text=str(gridCal[4][0][0]) + " , " + str(gridCal[4][0][1]), height = 5, width = 12, relief = "raised")
Label22 = Label (root, text=str(gridCal[4][1][0]) + " , " + str(gridCal[4][1][1]), height = 5, width = 12, relief = "raised")
Label23 = Label (root, text=str(gridCal[4][2][0]) + " , " + str(gridCal[4][2][1]), height = 5, width = 12, relief = "raised")
Label24 = Label (root, text=str(gridCal[4][3][0]) + " , " + str(gridCal[4][3][1]), height = 5, width = 12, relief = "raised")
Label25 = Label (root, text=str(gridCal[4][4][0]) + " , " + str(gridCal[4][4][1]), height = 5, width = 12, relief = "raised")

# Radio Buttons

Radio01 = Radiobutton(root, text="#01", variable=gridPos, value=1)
Radio02 = Radiobutton(root, text="#02", variable=gridPos, value=2)
Radio03 = Radiobutton(root, text="#03", variable=gridPos, value=3)
Radio04 = Radiobutton(root, text="#04", variable=gridPos, value=4)
Radio05 = Radiobutton(root, text="#05", variable=gridPos, value=5)
Radio06 = Radiobutton(root, text="#06", variable=gridPos, value=8)
Radio07 = Radiobutton(root, text="#07", variable=gridPos, value=7)
Radio08 = Radiobutton(root, text="#08", variable=gridPos, value=8)
Radio09 = Radiobutton(root, text="#09", variable=gridPos, value=9)
Radio10 = Radiobutton(root, text="#10", variable=gridPos, value=10)
Radio11 = Radiobutton(root, text="#11", variable=gridPos, value=11)
Radio12 = Radiobutton(root, text="#12", variable=gridPos, value=12)
Radio13 = Radiobutton(root, text="#13", variable=gridPos, value=13)
Radio14 = Radiobutton(root, text="#14", variable=gridPos, value=14)
Radio15 = Radiobutton(root, text="#15", variable=gridPos, value=15)
Radio16 = Radiobutton(root, text="#16", variable=gridPos, value=16)
Radio17 = Radiobutton(root, text="#17", variable=gridPos, value=17)
Radio18 = Radiobutton(root, text="#18", variable=gridPos, value=18)
Radio19 = Radiobutton(root, text="#19", variable=gridPos, value=19)
Radio20 = Radiobutton(root, text="#20", variable=gridPos, value=20)
Radio21 = Radiobutton(root, text="#21", variable=gridPos, value=21)
Radio22 = Radiobutton(root, text="#22", variable=gridPos, value=22)
Radio23 = Radiobutton(root, text="#23", variable=gridPos, value=23)
Radio24 = Radiobutton(root, text="#24", variable=gridPos, value=24)
Radio25 = Radiobutton(root, text="#25", variable=gridPos, value=25)

# Buttons

button_back = Button(root, text="Back", padx=50, pady=20, command=backMove)
button_left = Button(root, text="Left", padx=42, pady=20, command=leftMove)
button_right = Button(root, text="Right", padx=37, pady=20, command=rightMove)
button_forward = Button(root, text="Forward", padx=27, pady=20, command=forwardMove)


# Put stuff on the screen

Label01.grid(row=4, column=1)
Label02.grid(row=4, column=3)
Label03.grid(row=4, column=5)
Label04.grid(row=4, column=7)
Label05.grid(row=4, column=9)
Label06.grid(row=3, column=1)
Label07.grid(row=3, column=3)
Label08.grid(row=3, column=5)
Label09.grid(row=3, column=7)
Label10.grid(row=3, column=9)
Label11.grid(row=2, column=1)
Label12.grid(row=2, column=3)
Label13.grid(row=2, column=5)
Label14.grid(row=2, column=7)
Label15.grid(row=2, column=9)
Label16.grid(row=1, column=1)
Label17.grid(row=1, column=3)
Label18.grid(row=1, column=5)
Label19.grid(row=1, column=7)
Label20.grid(row=1, column=9)
Label21.grid(row=0, column=1)
Label22.grid(row=0, column=3)
Label23.grid(row=0, column=5)
Label24.grid(row=0, column=7)
Label25.grid(row=0, column=9)

Radio01.grid(row=4, column=0)
Radio02.grid(row=4, column=2)
Radio03.grid(row=4, column=4)
Radio04.grid(row=4, column=6)
Radio05.grid(row=4, column=8)
Radio06.grid(row=3, column=0)
Radio07.grid(row=3, column=2)
Radio08.grid(row=3, column=4)
Radio09.grid(row=3, column=6)
Radio10.grid(row=3, column=8)
Radio11.grid(row=2, column=0)
Radio12.grid(row=2, column=2)
Radio13.grid(row=2, column=4)
Radio14.grid(row=2, column=6)
Radio15.grid(row=2, column=8)
Radio16.grid(row=1, column=0)
Radio17.grid(row=1, column=2)
Radio18.grid(row=1, column=4)
Radio19.grid(row=1, column=6)
Radio20.grid(row=1, column=8)
Radio21.grid(row=0, column=0)
Radio22.grid(row=0, column=2)
Radio23.grid(row=0, column=4)
Radio24.grid(row=0, column=6)
Radio25.grid(row=0, column=8)

button_back.grid(row=6, column=5)
button_left.grid(row=7, column=3)
button_right.grid(row=7, column=7)
button_forward.grid(row=8, column=5)


f = open("GridCalibrationTable.txt", "w", )
f.write(str(gridCal.tolist()))
f.close()

print(gridCal[gridMap[1]])

root.mainloop()

