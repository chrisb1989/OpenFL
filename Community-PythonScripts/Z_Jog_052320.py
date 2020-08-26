# -*- coding: utf-8 -*-

from Tkinter import *
from OpenFL import Printer, FLP
import time


p=Printer.Printer() #change to Printer.Printer before using
p._command(Printer.Command.CMD_INITIALIZE, wait=False, expect_success=True)
root = Tk()
root.title('Z Jogger')

offsetList = [187310.0]
print("Current Z Position = "+ str(-1*(sum(offsetList))/1000.0))

#This section sets the read and write parameters for USB communication, according to the settings above

def writeUSB(data):
	return dev.write(RX_EP, data, timeout=None)

def readUSB(buffsize=1024):
	return dev.read(TX_EP, buffsize, timeout=10000)

def upMove():
	global jog
	jog = incrementZ.get()
	offsetList.append(float(jog)*2.5)
	print("Current Z Position = "+ str(-1*(sum(offsetList))/1000.0))
	p.move_z(jog, 4000)

def dnMove():
	global jog
	jog = (incrementZ.get())* -1.0
	offsetList.append(float(jog)*2.5)
	print("Current Z Position = "+ str(-1*(sum(offsetList))/1000.0))
	p.move_z(jog, 4000)

def goHome():
	p._command(Printer.Command.CMD_INITIALIZE, wait=False, expect_success=True)
	time.sleep(10)
	offsetList = []
	offsetList.append(187310.0)
	print("Current Z Position = "+ str(-1*(sum(offsetList))/1000.0))

def setZ():
	ZOffset = (-1*(sum(offsetList))/1000.0)
	fileName = "   /user.ini"
	blankSpace = bytearray(118)
	fineTuning="""   [serializerSettings]
	zOffset=""" + str(ZOffset) +"""


	[userSettings]
	xOffset=0
	xScale3=1
	yOffset=0
	yScale3=1
	\n
	"""
	fineTuningEncoded=bytearray(fileName)+blankSpace+bytearray(fineTuning)
	print("Saving Z Offset to Form1")
	p._command(Printer.Command.CMD_WRITE_FILE, fineTuningEncoded, expect_success=False, verbose=True)
	print("Z Offset is now set to "+ str(-1*(sum(offsetList))/1000.0))

def gotoSleep():
	p._command(Printer.Command.CMD_INITIALIZE, wait=False, expect_success=True)
	print("goodbye!")
	root.destroy()



incrementZ = IntVar()
incrementZ.set("20")

# define buttons

button_up = Button(root, text="Z Up", padx=50, pady=20, command=upMove)
button_down = Button(root, text="Z Down", padx=42, pady=20, command=dnMove)
button_home = Button(root, text="Home All", padx=37, pady=20, command=goHome)
button_SetZOffset = Button(root, text="Set Z Offset", padx=27, pady=20, command=setZ)
button_Exit = Button(root, text="Exit", padx=37, pady=20, command=gotoSleep)


# define radio buttons

Radio50 = Radiobutton(root, text="50 micron    ", variable=incrementZ, value=20)
Radio100 = Radiobutton(root, text="100 micron  ", variable=incrementZ, value=40)
Radio1000 = Radiobutton(root, text="1 millimeter ", variable=incrementZ, value=400)
Radio5000 = Radiobutton(root, text="5 millimeter ", variable=incrementZ, value=2000)


# Put buttons on the screen

button_up.grid(row=4, column=0)
button_down.grid(row=5, column=0)
button_home.grid(row=6, column=0)
button_SetZOffset.grid(row=7, column=0)
button_Exit.grid(row=8, column=0)
Radio50.grid(row=0, column=0)
Radio100.grid(row=1, column=0)
Radio1000.grid(row=2, column=0)
Radio5000.grid(row=3, column=0)


root.mainloop()

