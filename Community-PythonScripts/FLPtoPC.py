from OpenFL import Printer, FLP
import os
from datetime import datetime


#create directory and change to new directory 
blocksDir = os.path.join(os.getcwd(), "blocks" ,datetime.now().strftime('%Y-%m-%d_%H-%M'))
try:
	os.makedirs(blocksDir)
except:
	pass

os.chdir(blocksDir)

startTime = datetime.now()
print("start time is "+str(startTime))
p=Printer.Printer()

lastBlock=len(p.list_blocks())-1
layerNum=0

while layerNum <= lastBlock:
	layerStartTime = datetime.now()
	block=p.read_block_flp(layerNum)
	FLP.Packets(block).tofile(str(layerNum).zfill(8)+'.flp')
	print("block # "+str(layerNum)+" out of "+ str(lastBlock)+" saved in " + str(datetime.now() - layerStartTime))
	layerNum += 1

print("Total time to complete script was " + str(datetime.now() - startTime))