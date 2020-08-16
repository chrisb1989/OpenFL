# -*- coding: utf-8 -*-

from Tkinter import *
from OpenFL import Printer, FLP
import copy
import numpy as np


p=Printer.DummyPrinter() #change to Printer.Printer before using
root = Tk()
# name of the Tkinter window:
root.title('XY Calibration Tool')

# use ravel to flatten the grid table to 1D
gridCal = np.ravel(p.read_grid_table())

#set radio buttons to be integers
gridPos = IntVar()
#set default radio button to be front left position
gridPos.set("0")

tickNumber = IntVar()
tickNumber.set("10")

def backMove():
	global jogX
	global jogY
	""" 
	The radio button value is used for selecting the calibration grid point to edit.
	Even numbers (0-48) are X coordinates (front to back on F1+),
	Odd numbers (1-49) are Y coordinates (left to right on F1+).

	"""
	gridCal[gridPos.get()]  = gridCal[gridPos.get()] + tickNumber.get()
	jogX = gridCal[gridPos.get()]
	jogY = gridCal[gridPos.get() + 1]
	#p.set_laser_uint16(jogX, jogY) #uncomment for use with printer
	print (jogX)

def leftMove():
	global jogX
	global jogY
	""" 
	The radio button value is used for selecting the calibration grid point to edit.
	Even numbers (0-48) are X coordinates (front to back on F1+),
	Odd numbers (1-49) are Y coordinates (left to right on F1+).

	"""
	gridCal[gridPos.get() +1]  = gridCal[gridPos.get() +1] - tickNumber.get()
	jogX = gridCal[gridPos.get()]
	jogY = gridCal[gridPos.get() + 1]
	#p.set_laser_uint16(jogX, jogY) #uncomment for use with printer
	print (jogY)

def rightMove():
	global jogX
	global jogY
	""" 
	The radio button value is used for selecting the calibration grid point to edit.
	Even numbers (0-48) are X coordinates (front to back on F1+),
	Odd numbers (1-49) are Y coordinates (left to right on F1+).

	"""
	gridCal[gridPos.get() +1]  = gridCal[gridPos.get() +1] + tickNumber.get()
	jogX = gridCal[gridPos.get()]
	jogY = gridCal[gridPos.get() + 1]
	#p.set_laser_uint16(jogX, jogY) #uncomment for use with printer
	print (jogY)

def forwardMove():
	global jogX
	global jogY
	""" 
	The radio button value is used for selecting the calibration grid point to edit.
	Even numbers (0-48) are X coordinates (front to back on F1+),
	Odd numbers (1-49) are Y coordinates (left to right on F1+).

	"""
	gridCal[gridPos.get()]  = gridCal[gridPos.get()] - tickNumber.get()
	jogX = gridCal[gridPos.get()]
	jogY = gridCal[gridPos.get() + 1]
	#p.set_laser_uint16(jogX, jogY) #uncomment for use with printer
	print (jogX)

def saveGrid():
	# create or open a file called GridCalibrationTable.txt in same directory as this script
	f = open("GridCalibrationTable.txt", "w", )
	# reshape the calibration grid back to 5x5x2 and save/overwrite the file we just opened
	f.write(str(np.reshape(gridCal, (5,5,2)).tolist()))
	f.close()

""" 

This section defines Calibration Point Labels.

The calibration points are arranged from left to right and front to back from 1 to 25.

NOTE: These should dynamically update in the GUI - Need to fix this.

"""

Label01 = Label (root, text=str(gridCal[0]) + " , " + str(gridCal[1]), height = 5, width = 12, relief = "raised")
Label02 = Label (root, text=str(gridCal[2]) + " , " + str(gridCal[3]), height = 5, width = 12, relief = "raised")
Label03 = Label (root, text=str(gridCal[4]) + " , " + str(gridCal[5]), height = 5, width = 12, relief = "raised")
Label04 = Label (root, text=str(gridCal[6]) + " , " + str(gridCal[7]), height = 5, width = 12, relief = "raised")
Label05 = Label (root, text=str(gridCal[8]) + " , " + str(gridCal[9]), height = 5, width = 12, relief = "raised")
Label06 = Label (root, text=str(gridCal[10]) + " , " + str(gridCal[11]), height = 5, width = 12, relief = "raised")
Label07 = Label (root, text=str(gridCal[12]) + " , " + str(gridCal[13]), height = 5, width = 12, relief = "raised")
Label08 = Label (root, text=str(gridCal[14]) + " , " + str(gridCal[15]), height = 5, width = 12, relief = "raised")
Label09 = Label (root, text=str(gridCal[16]) + " , " + str(gridCal[17]), height = 5, width = 12, relief = "raised")
Label10 = Label (root, text=str(gridCal[18]) + " , " + str(gridCal[19]), height = 5, width = 12, relief = "raised")
Label11 = Label (root, text=str(gridCal[20]) + " , " + str(gridCal[21]), height = 5, width = 12, relief = "raised")
Label12 = Label (root, text=str(gridCal[22]) + " , " + str(gridCal[23]), height = 5, width = 12, relief = "raised")
Label13 = Label (root, text=str(gridCal[24]) + " , " + str(gridCal[25]), height = 5, width = 12, relief = "raised")
Label14 = Label (root, text=str(gridCal[26]) + " , " + str(gridCal[27]), height = 5, width = 12, relief = "raised")
Label15 = Label (root, text=str(gridCal[28]) + " , " + str(gridCal[29]), height = 5, width = 12, relief = "raised")
Label16 = Label (root, text=str(gridCal[30]) + " , " + str(gridCal[31]), height = 5, width = 12, relief = "raised")
Label17 = Label (root, text=str(gridCal[32]) + " , " + str(gridCal[33]), height = 5, width = 12, relief = "raised")
Label18 = Label (root, text=str(gridCal[34]) + " , " + str(gridCal[35]), height = 5, width = 12, relief = "raised")
Label19 = Label (root, text=str(gridCal[36]) + " , " + str(gridCal[37]), height = 5, width = 12, relief = "raised")
Label20 = Label (root, text=str(gridCal[38]) + " , " + str(gridCal[39]), height = 5, width = 12, relief = "raised")
Label21 = Label (root, text=str(gridCal[40]) + " , " + str(gridCal[41]), height = 5, width = 12, relief = "raised")
Label22 = Label (root, text=str(gridCal[42]) + " , " + str(gridCal[43]), height = 5, width = 12, relief = "raised")
Label23 = Label (root, text=str(gridCal[44]) + " , " + str(gridCal[45]), height = 5, width = 12, relief = "raised")
Label24 = Label (root, text=str(gridCal[46]) + " , " + str(gridCal[47]), height = 5, width = 12, relief = "raised")
Label25 = Label (root, text=str(gridCal[48]) + " , " + str(gridCal[49]), height = 5, width = 12, relief = "raised")

# Grid point radio buttons - These are for selecting a grid point to edit. 

Radio01 = Radiobutton(root, text="#01", variable=gridPos, value=0)
Radio02 = Radiobutton(root, text="#02", variable=gridPos, value=2)
Radio03 = Radiobutton(root, text="#03", variable=gridPos, value=4)
Radio04 = Radiobutton(root, text="#04", variable=gridPos, value=6)
Radio05 = Radiobutton(root, text="#05", variable=gridPos, value=8)
Radio06 = Radiobutton(root, text="#06", variable=gridPos, value=10)
Radio07 = Radiobutton(root, text="#07", variable=gridPos, value=12)
Radio08 = Radiobutton(root, text="#08", variable=gridPos, value=14)
Radio09 = Radiobutton(root, text="#09", variable=gridPos, value=16)
Radio10 = Radiobutton(root, text="#10", variable=gridPos, value=18)
Radio11 = Radiobutton(root, text="#11", variable=gridPos, value=20)
Radio12 = Radiobutton(root, text="#12", variable=gridPos, value=22)
Radio13 = Radiobutton(root, text="#13", variable=gridPos, value=24)
Radio14 = Radiobutton(root, text="#14", variable=gridPos, value=26)
Radio15 = Radiobutton(root, text="#15", variable=gridPos, value=28)
Radio16 = Radiobutton(root, text="#16", variable=gridPos, value=30)
Radio17 = Radiobutton(root, text="#17", variable=gridPos, value=32)
Radio18 = Radiobutton(root, text="#18", variable=gridPos, value=34)
Radio19 = Radiobutton(root, text="#19", variable=gridPos, value=36)
Radio20 = Radiobutton(root, text="#20", variable=gridPos, value=38)
Radio21 = Radiobutton(root, text="#21", variable=gridPos, value=40)
Radio22 = Radiobutton(root, text="#22", variable=gridPos, value=42)
Radio23 = Radiobutton(root, text="#23", variable=gridPos, value=44)
Radio24 = Radiobutton(root, text="#24", variable=gridPos, value=46)
Radio25 = Radiobutton(root, text="#25", variable=gridPos, value=48)

# Increment value radio buttons - these define the number of ticks the buttons will increment by:
RadioTick001 = Radiobutton(root, text="1 tick", variable=tickNumber, value=1)
RadioTick010 = Radiobutton(root, text="10 ticks", variable=tickNumber, value=10)
RadioTick100 = Radiobutton(root, text="100 ticks", variable=tickNumber, value=100)

# Increment buttons - these move the laser spot around:

button_back = Button(root, text="Back", padx=50, pady=20, command=backMove)
button_left = Button(root, text="Left", padx=42, pady=20, command=leftMove)
button_right = Button(root, text="Right", padx=37, pady=20, command=rightMove)
button_forward = Button(root, text="Forward", padx=27, pady=20, command=forwardMove)

# Save Button - This button saves the updated grid calibration to a file on your computer
button_save = Button(root, text="Save", padx=27, pady=20, command=saveGrid)



# Put stuff on the screen - This section arranges the Tkinter GUI elements on the screen

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
RadioTick001.grid(row=6, column=1)
RadioTick010.grid(row=7, column=1)
RadioTick100.grid(row=8, column=1)


button_back.grid(row=6, column=5)
button_left.grid(row=7, column=3)
button_right.grid(row=7, column=7)
button_forward.grid(row=8, column=5)
button_save.grid(row=9, column =5)

# This is the end of the Tkinter loop
root.mainloop()

