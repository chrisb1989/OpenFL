from OpenFL import FLP, Printer
from tenacity import retry
from tenacity import wait_fixed



p=Printer.Printer()

''' 
This defines a retry (Tenacity) function for writing blocks to the printer. If an exception is raised, the script will wait 2 seconds and try again.
Install tenacity via pip before running this script. Also, make sure you're using a 0.05mm vertical lift print profile.
'''

@retry
def writeLayer(wait=wait_fixed(2)):
	p.write_block_flp(blockNum, layer)

'''Initialize first - it seems to increase success rate of the script. Initializing stops any operations that are current running, and re homes the Z and tilt motors.
'''

print ("initializing")
p.initialize()

blockNum = 1
lastBlock = (len(p.list_blocks()) -1)

''' This loop changes two lines and adds a third line in each block (layer) on the printer. It checks to see if the value has already 
been set before trying to change it.
Summary of changes:
1) First, it changes the Z feed rate in line 5
2) Next, it inserts a positive Z move of 2000 usteps (5mm)
3) Lastly, it changes the Z move in layer 9 to -1960 (-4.9mm)
Note that in this case, positive values move the build plate away from the vat, and negative values move the build plate closer to the vat.
loop continues until it gets to the last block on the printer and then it ends.
'''
print ("starting loop")
while blockNum <= lastBlock:

        layer = p.read_block_flp(blockNum)

        if str(layer[5]) != '0x04 ZFeedRate '+str(267):
                try:
                        layer[5] = FLP.ZFeedRate(267)
                except:
                        break
        if str(layer[6]) != '0x03 ZMove '+str(2000):
                try:
                        layer.insert(6, FLP.ZMove(usteps=(2000)))
                except:
                        break
        if str(layer[9]) != '0x03 ZMove '+str(-1980):
                try:
                        layer[9] = FLP.ZMove(usteps=(-1980))
                except:
                        break
        writeLayer()
        print ("Layer " + str(blockNum) +" finished")
        blockNum += 1

print ("script ended at layer " + str(blockNum) +" out of " + str(lastBlock))
p.initialize()
exit()

