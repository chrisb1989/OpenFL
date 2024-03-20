#!/usr/bin/python
# -*- coding: utf-8 -*-

# A Grid Calibration Tool (AGCT) for Form1+ digital galvos
# Copyright 2020, Photonsters
# Micah Vestal [Lavachemist] and Jarrod Smith [MakerMatrix]
#
# Licensed under the Apache License
# https://www.apache.org/licenses/LICENSE-2.0.txt
#
# Wear laser glasses or you'll put your eye out:  8-)  ||  X-{

import time
#from Tkinter import * # python 2.7
#import tkMessageBox as mb # python 2.7
from tkinter import * # python 3
import tkinter.messagebox as mb # python 3
from OpenFL import Printer, FLP

################################################################################
# Functions, Global Variables
################################################################################
#Global button/scale state variables
gridButton=[[None for i in range(5)] for j in range(5)]
laserState = 0
laserText=["Toggle\nLaser On", "Toggle\nLaser Off"]
actRow = (None)
actCol = (None)
min_mW = 5  # Laser power min (default)
max_mW = 25 # Laser power max

#Initialize UI element values
default_font = "lucida 10 normal"
actBgColor = "#942323"
actFgColor = "white"
visBgColor = "#137d3a"
visFgColor = "black"
gridPadX = 0
gridPadY = 10
jogPadX = 15
jogPadY = 15
grooveBorder = 3
reliefBorder = 3
lfGridPadX = 25 # X padding between the bottom two frames of the UI

################################################################################
def valueWarning():
	mb.showerror("Galvo Range Exceeded", \
		"Dave, Stop.						 \nStop, will you?\nStop, Dave.")
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
def updateStatus(msg):

	statusLabel.config(text=msg)
	return()
################################################################################
def gridBtnPress(row, col):
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
	
	# Turn the laser on no matter what, by sending 1
	updateLaser(1)
	
	return()
################################################################################
def jogLaser(axis, direction):
	global actRow
	global actCol

	if laserState == 0:
		mb.showerror("Error: No laser spot", "Please activate the laser.")
		return()

	newValue = calGrid[actRow][actCol][axis] + (direction*jogSize.get())
	if ((newValue < 0) or ( newValue > 65535)):
		valueWarning()
	else:
		calGrid[actRow][actCol][axis] = newValue # Store the new ticks value
		updateLaser(1)  # Update the laser 

	return()
################################################################################
def cursorKey(event):
	
	direction = event.keysym
	
	if direction == "Up":
		jogLaser(0, 1)
	elif direction == "Down":
		jogLaser(0,-1)
	elif direction == "Left":
		jogLaser(1,-1)
	elif direction == "Right":
		jogLaser(1, 1)
	else: # Should never get here
		print ("ERROR in keybinding code.  Shutting down")
		p.shutdown()
		exit()
		
	return()
###############################################################################
def updateLaser(state=0):
	# Update the laser power, position, UI elements.
	# The state parameter can be 0 (off) or not 0 (on)
	global actRow
	global actCol
	global laserState
	
	# If we don't know where the laser should point yet, do nothing
	if (actRow is None) or (actCol is None):
		return()

	# Get current position in ticks
	xticks, yticks = calGrid[actRow][actCol]
	
	# Update the active grid button text with current tick values
	myLabel = "X=" + '{:05d}'.format(xticks) + "\n"
	myLabel += "Y=" + '{:05d}'.format(yticks)
	gridButton[actRow][actCol].config(text=myLabel)
	
	# Get the current laser power slider value
	my_mW = laserSlider.get()
	
	if state == 0:
		# Move the galvos, turn the laser off, update the UI.
		updateStatus("The laser is OFF")
		laserState = 0
		laserBtn.config(text=laserText[laserState], bg="gray85", fg="black")
		laserBtn.config(activeforeground="black", activebackground="gray95")
		laserSlider.config(fg="black", troughcolor="#AFAFAF")
		gridButton[actRow][actCol].config(bg=visBgColor, fg = visFgColor)
		try:
			p.set_laser_sint16(xticks, yticks, 0)
		except:
			pass # Currently must ignore these exceptions because brokenness ensues
	else:
		# Update the laser power, move the galvos, and update the UI
		msg = "The laser is ON with power = " + str(my_mW) + "mW"
		msg += "  |  Center the spot on the active target"
		updateStatus(msg)
		laserState=1
		laserBtn.config(text=laserText[laserState], bg=actBgColor)
		laserBtn.config(activeforeground=actFgColor, activebackground=actBgColor)
		laserSlider.config(fg=actBgColor, troughcolor=actBgColor)
		laserPower_ticks = int(p.mW_to_ticks(my_mW))
		gridButton[actRow][actCol].config(bg=actBgColor, fg = actFgColor)
		try:
			p.set_laser_uint16(xticks, yticks, laserPower_ticks)
		except:
			pass # Currently must ignore these exceptions because brokenness ensues
	return()
################################################################################
def updatePower(mW_str):
	# This is just a wrapper, we are really letting updateLaser handle
	# this because Scale() insists on sending its value as a string parameter.
	global laserState
	updateLaser(laserState)
	return()
################################################################################	
def toggleLaser():
	global actRow
	global actCol
	global laserState
	
	# Make the center point active if there is not an active gridpoint
	if (actRow is None) or (actCol is None):
		actRow = 2
		actCol = 2
		gridButton[actRow][actCol].invoke()
		return() # invoking the gridButton will turn it on, we're done
	
	if laserState == 0:
		# Turn the laser on.
		updateLaser(1)
	else:
		# Turn the laser off but leave the mW slider alone
		updateLaser(0)
		
	return()
################################################################################
def inspectGrid():
	# Loop over all targets and allow the user to inspect the alignment as
	# a final check.  Turns the laser off when finished.
	global actRow
	global actCol
	global laserState
	
	# remember current state and init some useful values
	entryRow = actRow
	entryCol = actCol
	entryLaserState = laserState
	targetNum = 0
	ntargets = 25
	sleepsecs = 2
	totalsecs = sleepsecs * ntargets
	
	# This takes awhile.  Disable the UI so users can't fuck up
	disableUI(root)
	statusLabel.config(state=NORMAL) # But turn the status bar back on
	
	#Start with the laser off and the current (if any) UI button deactivated
	updateLaser(0)
	
	for row in range(5):
		for col in range(5):
			actRow = row
			actCol = col
			targetNum += 1
			remainingTime = totalsecs + 2 - (targetNum * sleepsecs)
			bgColor = gridButton[row][col]["bg"] # remember bg color
			fgColor = gridButton[row][col]["fg"] # rember fg color
			updateLaser(1)
			statusMsg = "Performing scan, illuminating target "
			statusMsg += str(targetNum) + "/25 ("
			statusMsg += str(remainingTime) + "s remaining)."
			updateStatus(statusMsg)
			root.update() # Update the UI each time through so we can see
			time.sleep(sleepsecs)
			gridButton[row][col]["bg"] = bgColor # reset bg color
			gridButton[row][col]["fg"] = fgColor # reset fg color
			
	# Reset state
	toggleLaser()
	gridButton[row][col]["bg"] = bgColor # reset bg color
	gridButton[row][col]["fg"] = fgColor # reset fg color
	actRow = entryRow # Reset active row/col to what they were before
	actCol = entryCol
	laserState = entryLaserState
	updateStatus("Calibration target scan is complete.  The laser is OFF.")
	enableUI(root)
	return()
	
################################################################################
def saveGrid(calGrid):
	fName = "GridCalibrationTable.txt"
	# create or open a file called GridCalibrationTable.txt in same directory as this script
	f = open(fName, "w")
	# reshape the calibration grid array back to 5x5x2 and save/overwrite the file we just opened
	f.write(str(calGrid.tolist()))
	updateStatus("Wrote calibration grid to " + str(fName))
	f.close()
	return()
################################################################################	
def uiFrames():
	# Set up UI frames, as globals
	global gridFrame
	global laserFrame
	global rightLaserFrame
	global leftLaserFrame
	global jogSizeFrame
	
	# Frame Layout:  The root frame contains two frames - One on top for the
	# grid and one on bottom for all the laser controls.
	# The laser controls frame also contains two frames - one for the laser
	# jog/toggle buttons, laser slider and another one for the jogsize
	# radio buttons, Inspect, and Save.
	
	# This will keep things centered on the main window
	root.columnconfigure(0, weight=1)
	
	# All the grid target buttons go in this frame
	gridFrame = LabelFrame(root, text=" Choose A Target ", bd=3, pady=5, padx=5, labelanchor=N, relief=RIDGE)
	gridFrame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
	for col in range(5):
		gridFrame.columnconfigure(col, weight=1)

	# All the laser controls go in another frame
	laserFrame = LabelFrame(root, text=" Laser Controls ")
	laserFrame.config(bd=3, padx=10, pady=10, labelanchor=N, relief=RIDGE)
	laserFrame.grid(row=0, column=1, pady=10, padx=10, sticky=NSEW)
	# Make it so our subframes equally distribute across the X dimension
	laserFrame.columnconfigure(0, weight=1)
	laserFrame.columnconfigure(1, weight=1)
	
	# A sub frame for the jog/toggle buttons and power slider (left)
	leftLaserFrame = Frame(laserFrame, relief=FLAT)
	leftLaserFrame.config(padx=10, pady=10, bd=0)
	leftLaserFrame.grid(row=0, column=0, rowspan=2, padx=lfGridPadX, sticky=NE)
	
	# A sub frame for the jogsize radio buttons and Inspect/Save (right)
	rightLaserFrame = Frame(laserFrame, relief=FLAT)
	rightLaserFrame.config(padx=10, pady=0, bd=0)
	rightLaserFrame.grid(row=0, column=1, padx = lfGridPadX, sticky=NW)
	# Make it so any objects equally distribute across the Y dimension
	rightLaserFrame.columnconfigure(0, weight=1)
	
	# A subframe for the jog tick sizes (right)
	jogSizeFrame = LabelFrame(rightLaserFrame, text="Galvo Ticks\nPer Move", relief=GROOVE)
	jogSizeFrame.config(padx=10, pady=0, bd=1, labelanchor=N)
	jogSizeFrame.grid(row=0, column=1, padx=10, pady=10)
	return()
################################################################################
def mkGridButtons():
	# Builds the calibration grid UI as a 2D array of
	# tkinter Button()s indexed like [row][col]
	global gridButton

	for row in range(5):
		for col in range(5):
			thisLabel = "X=" + '{:05d}'.format(calGrid[row][col][0]) + "\n"
			thisLabel += "Y=" + '{:05d}'.format(calGrid[row][col][1])
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
	return()
################################################################################
def mkJogButtons():	
	# Draw the jog buttons - these will move the laser spot around
	# B=back, F=forward, L=left, R=Right
	global jogFBtn
	global jogBBtn
	global jogLBtn
	global jogRBtn
	
	jogFBtn = Button(leftLaserFrame, text="X -", padx=jogPadX, pady=jogPadY, \
		borderwidth= reliefBorder)
	jogBBtn = Button(leftLaserFrame, text="X +", padx=jogPadX, pady=jogPadY, \
		borderwidth= reliefBorder)
	jogLBtn = Button(leftLaserFrame, text="Y -", padx=jogPadX, pady=jogPadY, \
		borderwidth=reliefBorder)
	jogRBtn = Button(leftLaserFrame, text="Y +", padx=jogPadX, pady=jogPadY, \
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
	return()
################################################################################
def mkJogSizeButtons():
	# Construct jog size radio buttons - galvo ticks per cursor button click
	# Use loop values as exponents to define a log range, e.g [10, 100, 1000]
	# Defaults to the value of jogTicks during the final loop iteration
	global jogSizeBtn
	global jogSize
	
	jogSizeBtn = []
	jogSize = IntVar() # Tk integer variable class for radio button control
	
	for jogIdx in range(4):
		jogSizeBtn.append(None) # Make an empty array element
		jogTicks = 10 ** jogIdx # Compute the tick size for this radio button
		btn = jogSizeBtn[jogIdx] = Radiobutton(jogSizeFrame, text=str(jogTicks))
		btn.config(variable=jogSize, value=jogTicks, pady=10)
		jogSize.set(jogTicks) # Set the size of each jog in galvo ticks
		btn.grid(row=3-jogIdx, column=0, sticky=W) # Draw them on row 5, start on col 1
	
	return()
################################################################################
def mkLaserControls():
	# Draw laser toggle button, power slider, inspect button
	global laserBtn
	global laserSlider
	global inspectButton
	
	# Laser on/off toggle button
	laserBtn = Button(leftLaserFrame, text=laserText[laserState], \
		borderwidth= reliefBorder)
	laserBtn.grid(row=1, column=1, sticky = NSEW)
	laserBtn.config(command = toggleLaser)

	# Laser power slider
	laserSlider = Scale(leftLaserFrame, from_=min_mW, to_=max_mW, length=180, width=20)
	laserSlider.config(tickinterval=5, label="Laser Power (mW)", orient=HORIZONTAL)
	laserSlider.config(command = updatePower)
	laserSlider.grid(row=3, column=0, columnspan=3, pady=10)
	laserSlider.set(min_mW)

	# Save and Inspect buttons
	inspectButton=Button(rightLaserFrame, text="Inspect", command=inspectGrid)
	inspectButton.grid(row=1, column=1, padx=10, pady=2, sticky=NSEW)
	saveButton=Button(rightLaserFrame, text="Save", command=lambda: saveGrid(calGrid))
	saveButton.grid(row=2, column=1, padx=10, pady=2, sticky=NSEW)
	return()
################################################################################

def setAbsoluteHeight():

	absoluteText = text=heightTextInput.get()
	
	if str.isdigit(absoluteText.replace(".", "", 1)) or str(absoluteText) == "": # checks if the input is an int or float
		move = float(absoluteText) - globals()['currentZHeight'] # Calculating the move distance
		moveHeightRelative(move)
	else:
		mb.showinfo(title="Wrong input format", message="Please input a number in the absolute height text box. \nUse \".\" with decimal numbers. Ex. \"140.3\"")
		return() #Give a message to the user, that they have not entered a proper int or float.
        
	updateZHeightDisplay()
	
	return()
    
def moveHeightRelative(move): #Takes a length to move in mm, which can be both a positive and negative number
	if not isinstance(p, Printer.DummyPrinter): # Making sure the ui works even though we're using a dummy printer
		fdrate = 2400
		intmove = int(move*mmToStepsMultiplier)
		p.move_z(steps=intmove, feedrate=fdrate)

	globals()['currentZHeight'] = globals()['currentZHeight']+(move)
	
	updateZHeightDisplay()
	return()

def updateZHeightDisplay():
	heightCurrentZLabel2.config(text=str(globals()['currentZHeight']))
	return()

def mkHeightControls():

	global heightFrame
	global heightCurrentZLabel2
	global heightTextInput
	global zJogSize
	global mmToStepsMultiplier
	global currentZHeight
	
    ## Height variables
	currentZHeight = 165.0 # Only used when using a dummy printer
	mmToStepsMultiplier = 400 # 400 steps per mm. That is what they have used from the vendor, i found.
    
	if not isinstance(p, Printer.DummyPrinter): # Making sure the ui boots up even though we're using a dummy printer
		currentZHeight = p.read_zsensor_height()
	
	## Main height frame
	heightFrame = LabelFrame(root, text=" Z Height Controls ", bd=3, pady=5, padx=5, labelanchor=N, relief=RIDGE)
	heightFrame.grid(row=1, column=0, pady=10, padx=10, sticky=NSEW)
	
	## Absolute height settings
	heightAbsoluteHeightFrame = LabelFrame(heightFrame, text="Absolute Height")
	heightAbsoluteHeightFrame.grid(row=0, column=0)
	
	heightSetBtn = Button(heightAbsoluteHeightFrame, text="Set height", borderwidth=reliefBorder, command=setAbsoluteHeight)
	heightSetBtn.grid(row=1, column=0, padx=3, pady=2)
	
	heightTextInput = Entry(heightAbsoluteHeightFrame, width=20, text=1, justify="right")
	heightTextInput.grid(row=0, column=0, padx=3, pady=2)
	heightTextInput.insert(0, "0") 
	
	heightAbsoluteInputLabel = Label(heightAbsoluteHeightFrame, text="mm")
	heightAbsoluteInputLabel.grid(row=0, column=1, padx=3, pady=2)
	
	
	
	## Relative height
	
	heightRelativeHeightFrame = LabelFrame(heightFrame, text="Relative Height")
	heightRelativeHeightFrame.grid(row=0, column=1)
	
	# Minus plus buttons
	mpBtnFrame = Frame(heightRelativeHeightFrame, relief=RAISED)
	mpBtnFrame.grid(row=1, column=0)
	
    
	heightPlusBtn = Button(mpBtnFrame, text="Z +", borderwidth=reliefBorder, width=3, command=lambda: moveHeightRelative(zJogSize.get()))
	heightPlusBtn.grid(row=0, column=0, padx=3, pady=2, sticky = NSEW)
	
	heightMinusBtn = Button(mpBtnFrame, text="Z -", borderwidth=reliefBorder, width=3, command=lambda: moveHeightRelative(zJogSize.get() * -1))
	heightMinusBtn.grid(row=0, column=1, padx=3, pady=2, sticky = NSEW)
	
	# Radio buttons for -/+
	sizeBtnFrame = Frame(heightRelativeHeightFrame, relief=RAISED)
	sizeBtnFrame.grid(row=0, column=0, sticky = NSEW)
	
	zJogSize = DoubleVar(value=0.1)
	
	zrbtn01 = Radiobutton(sizeBtnFrame, text="0.1mm", variable=zJogSize, value=0.1)
	zrbtn01.grid(row=0, column=0, sticky=W, padx=3, pady=2)
	
	zrbtn1 = Radiobutton(sizeBtnFrame, text="1mm", variable=zJogSize, value=1.0)
	zrbtn1.grid(row=0, column=1, sticky=W, padx=3, pady=2)
	
	zrbtn10 = Radiobutton(sizeBtnFrame, text="10mm", variable=zJogSize, value=10.0)
	zrbtn10.grid(row=0, column=2, sticky=W, padx=3, pady=2)
	
	
	
	## Current height display
	
	heightCurrentZLabel1 = Label(heightFrame, text="Current Z height: ")
	heightCurrentZLabel1.grid(row=1, column=0, sticky=E)
	
	heightCurrentFrame = Frame(heightFrame, relief=RAISED)
	heightCurrentFrame.grid(row=1, column=1, sticky=W)
	
	heightCurrentZLabel2 = Label(heightCurrentFrame, text="0")
	heightCurrentZLabel2.grid(row=0, column=0, sticky=W)
	
	heightCurrentZLabel3 = Label(heightCurrentFrame, text="mm")
	heightCurrentZLabel3.grid(row=0, column=1, sticky=W)
	
	return()
################################################################################	
def mkMenus():
	# Draw the menu, and a status bar
	global menubar
	global statusLabel
	
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

	# Status bar across the bottom of the window
	statusText ="Select a calibration target to fire the laser,"
	statusText += " or press Inspect to scan the grid."
	statusLabel = Label(root, text=statusText)
	statusLabel.config( pady=0, relief=RAISED, anchor=W, bd=2, bg="gray80")
	statusLabel.grid(row=3, column=0, columnspan=5, padx=0, pady=0, sticky=NSEW)
	return()
################################################################################	
def bindCursorKeys():
	# Key binding for jogging the laser with cursor keys
	root.bind('<Up>', cursorKey)
	root.bind('<Left>', cursorKey)
	root.bind('<Right>', cursorKey)
	root.bind('<Down>', cursorKey)
	return()
################################################################################	
def disableUI(parent):
	# Recursively disable all UI elements under a parent container (Frame, Menu)
	
	for child in parent.winfo_children(): # enumerates all child objects
		wtype = child.winfo_class() # returns the type of object
		# If the child is also a Frame or Menu, call ourself again with that
		if wtype in ('Frame','Labelframe','Menu'):
			disableUI(child)
		else:
			child.configure(state=DISABLED)
			
	return()
################################################################################	
def enableUI(parent):
	# Recursively enable all UI elements under a parent container (Frame, Menu)
	
	for child in parent.winfo_children(): # enumerates all child objects
		wtype = child.winfo_class() # returns the type of object
		# If the child is also a Frame or Menu, call ourself again with that
		if wtype in ('Frame','Labelframe','Menu'):
			enableUI(child)
		else:
			child.configure(state=NORMAL)
	return()
################################################################################
# End of Functions
################################################################################

################################################################################
# MAIN PROGRAM CODE STARTS HERE
################################################################################
p=Printer.Printer() # Uncomment for real printer
#p=Printer.DummyPrinter() #This is for testing, comment when using real printer
p.initialize()

root = Tk()
# name of the Tkinter window:
root.title('Photonsters Form 1+ Grid Calibration Tool')
root.option_add("*Font", default_font)
# use the Photonsters image as a window icon
img = Image("photo", file="Photonsters.gif")
root.tk.call('wm','iconphoto',root._w,img)

# Read the calibration grid from the printer
calGrid = p.read_grid_table()

# Build the UI
uiFrames()
mkGridButtons()
mkHeightControls()
mkJogButtons()
mkJogSizeButtons()
mkLaserControls()
mkMenus()
bindCursorKeys()
updateZHeightDisplay()

# Give the UI control of the application
root.mainloop()

p.shutdown()
