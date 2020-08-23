#!/usr/bin/python
# -*- coding: utf-8 -*-

# Grid calibration tool for Form1+ digital galvos
# Copyright 2020, Photonsters
# Micah Vestal [Lavachemist] and Jarrod Smith [MakerMatrix]
#
# Licensed under the Apache License
# https://www.apache.org/licenses/LICENSE-2.0.txt
#
# 8-) Wear laser glasses or you'll put your eye out -> X-{

from Tkinter import *
import tkMessageBox as mb
from OpenFL import Printer, FLP
#from functions import *

################################################################################
# Functions, Global Variables
################################################################################
#Global button state variables
gridButton=[[None for i in range(5)] for j in range(5)]
laserState = 0
laserText=["Toggle\nLaser On", "Toggle\nLaser Off"]
actRow = (None)
actCol = (None)

#Initiali e UI element values
actBgColor = "#942323"
actFgColor = "white"
visBgColor = "#137d3a"
visFgColor = "black"
gridPadY = 10
gridPadX = 0
jogPadX = 20
jogPadY = 20
grooveBorder = 3
reliefBorder = 3

################################################################################
def valueWarning():
    mb.showerror("Galvo Range Exceeded", \
        "Dave, Stop.                         \nStop, will you?\nStop, Dave.")
################################################################################
def helpAbout():
	mb.showinfo("About", """The Form 1+ Grid Calibration Tool
							Created by Photonsters.
							www.photonsters.org
							www.openfl.dev
						Copyright 2020 Photonsters

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0.txt

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
		                  """)
################################################################################
def gridBtnPress( row, col):
    global actRow
    global actCol

    try:
        gridButton[actRow][actCol].config(bg=visBgColor, fg = visFgColor)
    except:
        pass

    gridButton[row][col].config(bg=actBgColor, fg = actFgColor,
            activeforeground = actFgColor, activebackground=actBgColor)
    actRow = row
    actCol = col
    return()
################################################################################
def jogLaser(axis, direction):
    global actRow
    global actCol

    if laserState == 0:
        mb.showerror("Error: No laser spot", "Please activate the laser.")
        return()
    else:
        if (actRow is None) or (actCol is None):
            actRow = 2
            actCol = 2
            gridButton[actRow][actCol].invoke()

    newValue = calGrid[actRow][actCol][axis] + (direction*jogSize.get())
    if ((newValue < 0) or ( newValue > 65535)):
        valueWarning()
    else:
        calGrid[actRow][actCol][axis] = newValue # Store the new value
        x = calGrid[actRow][actCol][0] # Get galvo x coord
        y = calGrid[actRow][actCol][1] # Get galvo y coord
        myLabel = "x = " + '{:05d}'.format(x) + "\n"
        myLabel += "y = " + '{:05d}'.format(y)
        gridButton[actRow][actCol].config(text=myLabel) # Update the button text
        p.set_laser_uint16(x, y, laserPower_ticks)

    print calGrid[actRow][actCol][axis]
################################################################################
def backMoveKey(event):
	global jogX
	global jogY
	"""
	The radio button value is used for selecting the calibration grid point to edit.
	Even numbers (0-48) are X coordinates (front to back on F1+),
	Odd numbers (1-49) are Y coordinates (left to right on F1+).

	"""
	if gridCal[gridPos.get()] + nudeSize < 0:
		valueWarning()
	elif gridCal[gridPos.get()] + tickNumber.get() > 65535:
		valueWarning()
	else:
		gridCal[gridPos.get()]  = gridCal[gridPos.get()] + tickNumber.get()
		labelUpdate()
		jogX = gridCal[gridPos.get()]
		jogY = gridCal[gridPos.get() + 1]
		p.set_laser_uint16(jogX, jogY, power=laserPower_ticks) #uncomment for use with printer
	print (jogX)
################################################################################
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
		p.set_laser_uint16(jogX, jogY, power=laserPower_ticks) #uncomment for use with printer
	print (jogY)
################################################################################

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
		p.set_laser_uint16(jogX, jogY, power=laserPower_ticks) #uncomment for use with printer
	print (jogY)
################################################################################
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
		p.set_laser_uint16(jogX, jogY, power=laserPower_ticks) #uncomment for use with printer
	print (jogX)
################################################################################
def laserToggle():
    global actRow
    global actCol
    global laserState

    # Make the center point active if there is not an active gridpoint
    if (actRow is None) or (actCol is None):
        actRow = 2
        actCol = 2
        gridButton[actRow][actCol].invoke()
    #Get the current x,y positions
    xticks, yticks = calGrid[actRow][actCol]
    # Get the current laser power slider value
    my_mW = laserSlider.get()

    if laserState == 0:
        # We are going to turn the laser on.
        print("Turning on the Laser")
        laserPower_ticks = int(p.mW_to_ticks(my_mW))
        print("I've set laserPower_ticks to ", laserPower_ticks)
        p.set_laser_uint16(xticks, yticks, laserPower_ticks)
        laserState = 1
        laserBtn.config(text=laserText[laserState], bg=actBgColor)
        laserBtn.config(activeforeground=actFgColor, activebackground=actBgColor)
        laserSlider.config(fg=actBgColor, troughcolor=actBgColor)
    else:
        # The laser needs to be turned off but we leave the slider alone
        print("Turning off the laser")
        p.set_laser_uint16(xticks, yticks, 0)
        laserState = 0
        laserBtn.config(text=laserText[laserState], bg="gray85", fg="black")
        laserBtn.config(activeforeground="black", activebackground="gray95")
        laserSlider.config(fg="black", troughcolor="#AFAFAF")
    return (laserState)
################################################################################
def saveGrid(calGrid):
    fName = "GridCalibrationTable.txt"
	# create or open a file called GridCalibrationTable.txt in same directory as this script
    f = open(fName, "w")
	# reshape the calibration grid array back to 5x5x2 and save/overwrite the file we just opened
    f.write(str(calGrid.tolist()))
    print("Wrote calibration grid to " + str(fName))
    f.close()
################################################################################
# End of Functions
################################################################################

################################################################################
# MAIN PROGRAM CODE STARTS HERE
################################################################################
#p=Printer.Printer() # Uncomment for real printer
p=Printer.DummyPrinter() #This is for testing, comment when using real printer
p.initialize()

root = Tk()
# name of the Tkinter window:
root.title('Photonsters Form 1+ Grid Calibration Tool')
# use the Photonsters image as a window icon
img = Image("photo", file="Photonsters.gif")
root.tk.call('wm','iconphoto',root._w,img)

calGrid = p.read_grid_table()
print calGrid

# Key binding - still testing this
root.bind('<Up>', backMoveKey)
root.bind('<Left>', leftMoveKey)
root.bind('<Right>', rightMoveKey)
root.bind('<Down>', forwardMoveKey)

# Set up UI frames
gridFrame = LabelFrame(root, text=" Choose A Target ", bd=3, pady=5, padx=5, \
    labelanchor=N, relief=RIDGE)
gridFrame.grid(row=0, column=0, rowspan=5, columnspan=5, padx=10, pady=10)
laserFrame = LabelFrame(root, text=" Laser Controls ", labelanchor=N, relief=RIDGE)
laserFrame.config(bd=3, padx=20, pady=10)
laserFrame.grid(row=5, column=0, rowspan=4, columnspan=5, pady=10, padx=25, sticky=NSEW)
root.columnconfigure(0, weight=1)
spacerFrame = LabelFrame(laserFrame, text="Some Space", relief=GROOVE).grid(row=5,column=3)
spacerLabel=Label(spacerFrame, text="Some Space").grid(row=0,column=0)
spaceFrame = LabelFrame(laserFrame, text="Galvo Ticks\nPer Move", relief=GROOVE)
spaceFrame.config(padx=10, pady=10, bd=1, labelanchor=N)
spaceFrame.grid(row=0, column=3, rowspan=3, padx=10, pady=10, sticky=E)
jogSizeFrame = LabelFrame(laserFrame, text="Galvo Ticks\nPer Move", relief=GROOVE)
jogSizeFrame.config(padx=10, pady=10, bd=1, labelanchor=N)
jogSizeFrame.grid(row=0, column=4, rowspan=3, padx=10, pady=10, sticky=E)

# Builds the calibration grid UI as a 2D array of
# tkinter Button()s indexed like [row][col]
for row in range(5):
    for col in range(5):
        thisLabel = "x = " + '{:05d}'.format(calGrid[row][col][0]) + "\n"
        thisLabel += "y = " + '{:05d}'.format(calGrid[row][col][1])
        btn = gridButton[row][col] = Button(gridFrame, text=thisLabel, relief=GROOVE)
        btn.config(pady=gridPadY, activebackground=actBgColor, borderwidth=grooveBorder)
        btn.config(command = lambda r=row, c=col: gridBtnPress( r, c))
# Reverse the first grid button dimension (row indices) while we draw them
# so that the UI orientation matches the front-view printer orientation
gridButton.reverse()
for row in range(5):
    for col in range(5):
        gridButton[row][col].grid(row=row, column=col, padx=2, pady=2)
# Now put them back so they once again match their callback indices
gridButton.reverse()

# Jog buttons - these move the laser spot around
# B=back, F=forward, L=left, R=Right
jogFBtn = Button(laserFrame, text="X -", padx=jogPadX, pady=jogPadY, \
    borderwidth= reliefBorder)
jogBBtn = Button(laserFrame, text="X +", padx=jogPadX, pady=jogPadY, \
    borderwidth= reliefBorder)
jogLBtn = Button(laserFrame, text="Y -", padx=jogPadX, pady=jogPadY, \
    borderwidth=reliefBorder)
jogRBtn = Button(laserFrame, text="Y +", padx=jogPadX, pady=jogPadY, \
    borderwidth= reliefBorder)
# Jog callbacks
jogFBtn.config(command=lambda axis=0, direction=-1: jogLaser(axis, direction))
jogBBtn.config(command=lambda axis=0, direction=1: jogLaser(axis, direction))
jogLBtn.config(command=lambda axis=1, direction=-1: jogLaser(axis, direction))
jogRBtn.config(command=lambda axis=1, direction=1: jogLaser(axis, direction))
# Jog button grid arrangement
jogBBtn.grid(row=0, column=1, pady = jogPadY/2)
jogLBtn.grid(row=1, column=0, sticky = E, padx = jogPadX/2)
jogRBtn.grid(row=1, column=2, sticky = W, padx = jogPadX/2)
jogFBtn.grid(row=2, column=1, pady = jogPadY/2)

# Construct jog size radio buttons - galvo ticks per cursor button click
# Use loop values as exponents to define a log range, e.g [1, 10, 100]
# Defaults to the value of jogTicks during the final loop iteration
jogSizeBtn = []

jogSize = IntVar() # Tk integer variable class for radio button control
for jogIdx in range(3):
    jogSizeBtn.append(None) # Make an empty array element
    jogTicks = 10 ** jogIdx # Compute the tick size for this radio button
    btn = jogSizeBtn[jogIdx] = Radiobutton(jogSizeFrame, text=str(jogTicks))
    btn.config(variable=jogSize, value=jogTicks, pady=jogPadY)
    jogSize.set(jogTicks) # Set the size of each jog in galvo ticks
    btn.grid(row=2-jogIdx, column=0, sticky=W) # Draw them on row 5, start on col 1

# Laser power.  Allow a range of 5-25mW.  Default to 5mW
max_mW = 25
laserPower_mW = min_mW = 5
laserPower_ticks = int(p.mW_to_ticks(laserPower_mW))
print("Laser power is set to ", laserPower_mW, " mW (", laserPower_ticks, " ticks)")

# Laser on/off toggle button
laserBtn = Button(laserFrame, text=laserText[laserState], \
    borderwidth= reliefBorder)
laserBtn.grid(row=1, column=1, sticky = NSEW)
laserBtn.config(command = laserToggle)

# Laser power slider
laserSlider = Scale(laserFrame, from_=min_mW, to_=max_mW, length=180, width=20)
laserSlider.config(tickinterval=5, label="Laser Power (mW)", orient=HORIZONTAL)
laserSlider.grid(row=3, column=0, columnspan=3)
laserSlider.set(laserPower_mW)

scanButton=Button(laserFrame, text="Inspect")
scanButton.grid(row=3, column=4, padx=5, pady=5)

statusLabel = Label(root, text="Select a calibration target and fire the laser.")
statusLabel.config(width=72, pady=0, relief=RAISED, anchor=W, bd=2, bg="gray80")
statusLabel.grid(row=9, column=0, columnspan=5, padx=0, pady=0, sticky=SW)

# Build a menubar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command = lambda: saveGrid(calGrid))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command=helpAbout)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)

root.mainloop()

p.shutdown()

"""
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;; CREATED BY ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;; lavachemist ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;; and MakerMatrix ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;; enjoy! ;;;;;;;;;;;;;;;;   ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;      ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;        ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;     ;;;;;;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;  ;;;   ;;    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;  ;;   ;  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;;;;  ; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;;;;;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;  ;; ;;;;  ;; ;;  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;    ;;    ;;    ;  ;;  ;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;             ;     ;        ;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;   ;;                            ;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;    ;                                 ;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;   ;;;                             ;         ;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;     ;;       ;;                        ;;           ;;;;;;;;;;;;
;;;;;;;;;;;;      ;;;      ;;          ;       ;        ;;              ;;;;;;;;
;;;;          ;;;;       ;            ;                 ;;                ;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
"""
