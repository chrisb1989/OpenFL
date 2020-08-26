# -*- coding: utf-8 -*-
from OpenFL import Printer, FLP
import glob
import Tkinter, tkFileDialog
import os
from datetime import datetime

startTime = datetime.now()

root = Tkinter.Tk()
root.withdraw()
folderPath = tkFileDialog.askdirectory()
os.chdir(folderPath)

p=Printer.Printer()
p.initialize()
layerNum=0
lastBlock = (len(glob.glob("*.flp"))-1)


while layerNum <= lastBlock:
	layerStartTime = datetime.now()
	fileName =(str(layerNum).zfill(8)+'.flp')
	layer=FLP.fromfile(fileName)
	p.write_block_flp(layerNum, layer)
	print("layer " +str(layerNum)+ " of "+ str(lastBlock) + " saved in " + str(datetime.now() - layerStartTime))
	layerNum += 1
print("All FLP files written to Printer, total time to complete - "+str(datetime.now() - startTime))