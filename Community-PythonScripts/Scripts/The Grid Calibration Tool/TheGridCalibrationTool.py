# -*- coding: utf-8 -*-

from Tkinter import *
import tkMessageBox as mb
from OpenFL import Printer, FLP
import numpy as np


p=Printer.Printer() # Uncomment for real printer
#p=Printer.DummyPrinter() #This is for testing, comment when using real printer
p.initialize()

root = Tk()
# name of the Tkinter window:
root.title('Photonsters Form 1+ Grid Calibration Tool')
# use the Photonsters image as a window icon
#img = Image("photo", file="Photonsters.gif")
#root.tk.call('wm','iconphoto',root._w,img)

# use ravel to flatten the grid table to 1D
gridCal = np.ravel(p.read_grid_table())	

#set radio buttons to be integers
gridPos = IntVar()
tickNumber = IntVar()
tickNumber.set("100")

"""
This section is a list of variables used for dynamically updating the label text of the grid points
"""
textVar01 = StringVar()
textVar02 = StringVar()
textVar03 = StringVar()
textVar04 = StringVar()
textVar05 = StringVar()
textVar06 = StringVar()
textVar07 = StringVar()
textVar08 = StringVar()
textVar09 = StringVar()
textVar10 = StringVar()
textVar11 = StringVar()
textVar12 = StringVar()
textVar13 = StringVar()
textVar14 = StringVar()
textVar15 = StringVar()
textVar16 = StringVar()
textVar17 = StringVar()
textVar18 = StringVar()
textVar19 = StringVar()
textVar20 = StringVar()
textVar21 = StringVar()
textVar22 = StringVar()
textVar23 = StringVar()
textVar24 = StringVar()
textVar25 = StringVar()

# Functions:

def valueWarning():
    mb.showerror("Warning: Galvo Range Exceeded", "I'm sorry, I'm afraid I can't do that.")

def helpAbout():
	mb.showinfo("About", """The Form 1+ Grid Calibration Tool 
							Created by Photonsters. 
							www.photonsters.org
							www.openfl.dev
						Copyright 2020 Photonsters

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
		                  """)
	

def backMove():
	global jogX
	global jogY
	""" 
	The radio button value is used for selecting the calibration grid point to edit.
	Even numbers (0-48) are X coordinates (front to back on F1+),
	Odd numbers (1-49) are Y coordinates (left to right on F1+).

	"""
	if gridCal[gridPos.get()] + tickNumber.get() < 0:
		valueWarning()
	elif gridCal[gridPos.get()] + tickNumber.get() > 65535:
		valueWarning()
	else:
		gridCal[gridPos.get()]  = gridCal[gridPos.get()] + tickNumber.get()
		labelUpdate()
		jogX = gridCal[gridPos.get()]
		jogY = gridCal[gridPos.get() + 1]
		p.set_laser_uint16(jogX, jogY, power=laserPower) #uncomment for use with printer
	print (jogX)

def backMoveKey(event):
	global jogX
	global jogY
	""" 
	The radio button value is used for selecting the calibration grid point to edit.
	Even numbers (0-48) are X coordinates (front to back on F1+),
	Odd numbers (1-49) are Y coordinates (left to right on F1+).

	"""
	if gridCal[gridPos.get()] + tickNumber.get() < 0:
		valueWarning()
	elif gridCal[gridPos.get()] + tickNumber.get() > 65535:
		valueWarning()
	else:
		gridCal[gridPos.get()]  = gridCal[gridPos.get()] + tickNumber.get()
		labelUpdate()
		jogX = gridCal[gridPos.get()]
		jogY = gridCal[gridPos.get() + 1]
		p.set_laser_uint16(jogX, jogY, power=laserPower) #uncomment for use with printer
	print (jogX)


def leftMove():
	global jogX
	global jogY
	""" 
	The radio button value is used for selecting the calibration grid point to edit.
	Even numbers (0-48) are X coordinates (front to back on F1+),
	Odd numbers (1-49) are Y coordinates (left to right on F1+).

	"""
	if gridCal[gridPos.get() +1] - tickNumber.get() < 0:
		valueWarning()
	elif gridCal[gridPos.get() +1] + tickNumber.get() > 65535:
		valueWarning()
	else:
		gridCal[gridPos.get() +1]  = gridCal[gridPos.get() +1] - tickNumber.get()
		labelUpdate()
		jogX = gridCal[gridPos.get()]
		jogY = gridCal[gridPos.get() + 1]
		p.set_laser_uint16(jogX, jogY, power=laserPower) #uncomment for use with printer
	print (jogY)

def leftMoveKey(event):
	global jogX
	global jogY
	""" 
	The radio button value is used for selecting the calibration grid point to edit.
	Even numbers (0-48) are X coordinates (front to back on F1+),
	Odd numbers (1-49) are Y coordinates (left to right on F1+).

	"""
	if gridCal[gridPos.get() +1] - tickNumber.get() < 0:
		valueWarning()
	elif gridCal[gridPos.get() +1] + tickNumber.get() > 65535:
		valueWarning()
	else:
		gridCal[gridPos.get() +1]  = gridCal[gridPos.get() +1] - tickNumber.get()
		labelUpdate()
		jogX = gridCal[gridPos.get()]
		jogY = gridCal[gridPos.get() + 1]
		p.set_laser_uint16(jogX, jogY, power=laserPower) #uncomment for use with printer
	print (jogY)

def rightMove():
	global jogX
	global jogY
	""" 
	The radio button value is used for selecting the calibration grid point to edit.
	Even numbers (0-48) are X coordinates (front to back on F1+),
	Odd numbers (1-49) are Y coordinates (left to right on F1+).

	"""
	if gridCal[gridPos.get() +1] + tickNumber.get() < 0:
		valueWarning()
	elif gridCal[gridPos.get() +1] + tickNumber.get() > 65535:
		valueWarning()
	else:
		gridCal[gridPos.get() +1]  = gridCal[gridPos.get() +1] + tickNumber.get()
		labelUpdate()
		jogX = gridCal[gridPos.get()]
		jogY = gridCal[gridPos.get() + 1]
		p.set_laser_uint16(jogX, jogY, power=laserPower) #uncomment for use with printer
	print (jogY)

def rightMoveKey(event):
	global jogX
	global jogY
	""" 
	The radio button value is used for selecting the calibration grid point to edit.
	Even numbers (0-48) are X coordinates (front to back on F1+),
	Odd numbers (1-49) are Y coordinates (left to right on F1+).

	"""
	if gridCal[gridPos.get() +1] + tickNumber.get() < 0:
		valueWarning()
	elif gridCal[gridPos.get() +1] + tickNumber.get() > 65535:
		valueWarning()
	else:
		gridCal[gridPos.get() +1]  = gridCal[gridPos.get() +1] + tickNumber.get()
		labelUpdate()
		jogX = gridCal[gridPos.get()]
		jogY = gridCal[gridPos.get() + 1]
		p.set_laser_uint16(jogX, jogY, power=laserPower) #uncomment for use with printer
	print (jogY)

def forwardMove():
	global jogX
	global jogY
	""" 
	The radio button value is used for selecting the calibration grid point to edit.
	Even numbers (0-48) are X coordinates (front to back on F1+),
	Odd numbers (1-49) are Y coordinates (left to right on F1+).

	"""
	if gridCal[gridPos.get()] - tickNumber.get() < 0:
		valueWarning()
	elif gridCal[gridPos.get()] + tickNumber.get() > 65535:
		valueWarning()
	else:
		gridCal[gridPos.get()]  = gridCal[gridPos.get()] - tickNumber.get()
		labelUpdate()
		jogX = gridCal[gridPos.get()]
		jogY = gridCal[gridPos.get() + 1]
		p.set_laser_uint16(jogX, jogY, power=laserPower) #uncomment for use with printer
	print (jogX)

def forwardMoveKey(event):
	global jogX
	global jogY
	""" 
	The radio button value is used for selecting the calibration grid point to edit.
	Even numbers (0-48) are X coordinates (front to back on F1+),
	Odd numbers (1-49) are Y coordinates (left to right on F1+).

	"""
	if gridCal[gridPos.get()] - tickNumber.get() < 0:
		valueWarning()
	elif gridCal[gridPos.get()] + tickNumber.get() > 65535:
		valueWarning()
	else:
		gridCal[gridPos.get()]  = gridCal[gridPos.get()] - tickNumber.get()
		labelUpdate()
		jogX = gridCal[gridPos.get()]
		jogY = gridCal[gridPos.get() + 1]
		p.set_laser_uint16(jogX, jogY, power=laserPower) #uncomment for use with printer
	print (jogX)

def laserOn():
	p.set_laser_uint16(gridCal[gridPos.get()], gridCal[gridPos.get() +1], power=laserPower)

def saveGrid():
	# create or open a file called GridCalibrationTable.txt in same directory as this script
	f = open("GridCalibrationTable.txt", "w", )
	# reshape the calibration grid array back to 5x5x2 and save/overwrite the file we just opened
	f.write(str(np.reshape(gridCal, (5,5,2)).tolist()))
	f.close()

# This function sets the text variables for the labels

def labelUpdate():
	textVar01.set('x= '+str(gridCal[0])+'\n y= '+(str(gridCal[1])))
	textVar02.set('x= '+str(gridCal[2])+'\n y= '+(str(gridCal[3])))
	textVar03.set('x= '+str(gridCal[4])+'\n y= '+(str(gridCal[5])))
	textVar04.set('x= '+str(gridCal[6])+'\n y= '+(str(gridCal[7])))
	textVar05.set('x= '+str(gridCal[8])+'\n y= '+(str(gridCal[9])))
	textVar06.set('x= '+str(gridCal[10])+'\n y= '+(str(gridCal[11])))
	textVar07.set('x= '+str(gridCal[12])+'\n y= '+(str(gridCal[13])))
	textVar08.set('x= '+str(gridCal[14])+'\n y= '+(str(gridCal[14])))
	textVar09.set('x= '+str(gridCal[16])+'\n y= '+(str(gridCal[17])))
	textVar10.set('x= '+str(gridCal[18])+'\n y= '+(str(gridCal[19])))
	textVar11.set('x= '+str(gridCal[20])+'\n y= '+(str(gridCal[21])))
	textVar12.set('x= '+str(gridCal[22])+'\n y= '+(str(gridCal[23])))
	textVar13.set('x= '+str(gridCal[24])+'\n y= '+(str(gridCal[25])))
	textVar14.set('x= '+str(gridCal[26])+'\n y= '+(str(gridCal[27])))
	textVar15.set('x= '+str(gridCal[28])+'\n y= '+(str(gridCal[29])))
	textVar16.set('x= '+str(gridCal[30])+'\n y= '+(str(gridCal[31])))
	textVar17.set('x= '+str(gridCal[32])+'\n y= '+(str(gridCal[33])))
	textVar18.set('x= '+str(gridCal[34])+'\n y= '+(str(gridCal[25])))
	textVar19.set('x= '+str(gridCal[36])+'\n y= '+(str(gridCal[37])))
	textVar20.set('x= '+str(gridCal[38])+'\n y= '+(str(gridCal[39])))
	textVar21.set('x= '+str(gridCal[40])+'\n y= '+(str(gridCal[41])))
	textVar22.set('x= '+str(gridCal[42])+'\n y= '+(str(gridCal[43])))
	textVar23.set('x= '+str(gridCal[44])+'\n y= '+(str(gridCal[45])))
	textVar24.set('x= '+str(gridCal[46])+'\n y= '+(str(gridCal[47])))
	textVar25.set('x= '+str(gridCal[48])+'\n y= '+(str(gridCal[49])))

# Laser power setter
laserPower = 12500

# Key binding - still testing this

root.bind('<Up>', backMoveKey)
root.bind('<Left>', leftMoveKey)
root.bind('<Right>', rightMoveKey)
root.bind('<Down>', forwardMoveKey)


#Menus - still testing this stuff
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=saveGrid)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command=helpAbout)
menubar.add_cascade(label="Help", menu=helpmenu)

""" 

This section defines Calibration Point Labels.

The calibration points are arranged from left to right and front to back from 1 to 25.

NOTE: These should dynamically update in the GUI - Need to fix this.

"""

labelUpdate() # Update the labels so they aren't blank when script starts.

Label01 = Label (root, textvariable=textVar01, height = 5, width = 12, relief = "raised")
Label02 = Label (root, textvariable=textVar02, height = 5, width = 12, relief = "raised")
Label03 = Label (root, textvariable=textVar03, height = 5, width = 12, relief = "raised")
Label04 = Label (root, textvariable=textVar04, height = 5, width = 12, relief = "raised")
Label05 = Label (root, textvariable=textVar05, height = 5, width = 12, relief = "raised")
Label06 = Label (root, textvariable=textVar06, height = 5, width = 12, relief = "raised")
Label07 = Label (root, textvariable=textVar07, height = 5, width = 12, relief = "raised")
Label08 = Label (root, textvariable=textVar08, height = 5, width = 12, relief = "raised")
Label09 = Label (root, textvariable=textVar09, height = 5, width = 12, relief = "raised")
Label10 = Label (root, textvariable=textVar10, height = 5, width = 12, relief = "raised")
Label11 = Label (root, textvariable=textVar11, height = 5, width = 12, relief = "raised")
Label12 = Label (root, textvariable=textVar12, height = 5, width = 12, relief = "raised")
Label13 = Label (root, textvariable=textVar13, height = 5, width = 12, relief = "raised")
Label14 = Label (root, textvariable=textVar14, height = 5, width = 12, relief = "raised")
Label15 = Label (root, textvariable=textVar15, height = 5, width = 12, relief = "raised")
Label16 = Label (root, textvariable=textVar16, height = 5, width = 12, relief = "raised")
Label17 = Label (root, textvariable=textVar17, height = 5, width = 12, relief = "raised")
Label18 = Label (root, textvariable=textVar18, height = 5, width = 12, relief = "raised")
Label19 = Label (root, textvariable=textVar19, height = 5, width = 12, relief = "raised")
Label20 = Label (root, textvariable=textVar20, height = 5, width = 12, relief = "raised")
Label21 = Label (root, textvariable=textVar21, height = 5, width = 12, relief = "raised")
Label22 = Label (root, textvariable=textVar22, height = 5, width = 12, relief = "raised")
Label23 = Label (root, textvariable=textVar23, height = 5, width = 12, relief = "raised")
Label24 = Label (root, textvariable=textVar24, height = 5, width = 12, relief = "raised")
Label25 = Label (root, textvariable=textVar25, height = 5, width = 12, relief = "raised")

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
RadioTick200 = Radiobutton(root, text="200 ticks", variable=tickNumber, value=200)

# Increment buttons - these move the laser spot around:

button_back = Button(root, text="X +", padx=27, pady=20, command=backMove)
button_left = Button(root, text="Y -", padx=27, pady=20, command=leftMove)
button_right = Button(root, text="Y +", padx=27, pady=20, command=rightMove)
button_forward = Button(root, text="X -", padx=27, pady=20, command=forwardMove)
button_laser = Button(root, text="Laser On", padx=27, pady=20, command=laserOn)

# Save Button - This button saves the updated grid calibration to a file on your computer
button_save = Button(root, text="Save", padx=27, pady=20, command=saveGrid)



# Put stuff on the screen - This section arranges the Tkinter GUI elements on the screen

# Label arrangement
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

# radio button arrangement
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
RadioTick200.grid(row=9, column=1)

# button arrangement
button_back.grid(row=6, column=5)
button_left.grid(row=7, column=3)
button_laser.grid(row=7, column=5)
button_right.grid(row=7, column=7)
button_forward.grid(row=8, column=5)
button_save.grid(row=9, column =5)

# This section sets the text variable of the labels so they dynamically update - Not sure why they don't.

root.config(menu=menubar) # testing stuff
# This is the end of the Tkinter loop
root.mainloop()

p.shutdown()
