from OpenFL import Printer, FLP

# use this for a real printer:
p=Printer.Printer()

# OR

# use this for Dummy printer (comment out the start_printing command, or it might fail):
# p=Printer.DummyPrinter()

# variables (don't change these)
F=FLP
packets = F.Packets()
grid = p.read_grid_table()

if len(p.list_blocks()) >= 0:
	p.delete_block(0)

#packets.append(FLP.makeHomingSequence())
#packets.append(FLP.Dwell(2000))
packets.append(F.LayerStart(0))

# Main function
def flpMaker(x, y):
	# first turn off the laser and move to a point
	packets.append(F.XYMove([[x, y, 2000]]))
	# then turn on the laser for 5 seconds in ticks (60,000 * number of seconds)
	packets.append(F.LaserPowerLevel(32768))
	# increase or decrease the number in the command below for longer or shorter duration
	packets.append(F.XYMove([[x, y, 20000]]))
	# uncomment for button press between points
	#packets.append(F.WaitButtonPress("Press The Button!"))
	return packets

# Main Loop
for row in grid:
	for point in row:
		flpMaker(point[0], point[1])

# Send to printer
packets.append(F.LayerDone())
p.write_block_flp(0, packets)

# these are just for troubleshooting/viewing the FLP packet, comment to remove
layer = p.read_block_flp(0)
print(layer)

# comment this out if you are using a Dummy printer, and/or if you are just testing
p.start_printing(0)
