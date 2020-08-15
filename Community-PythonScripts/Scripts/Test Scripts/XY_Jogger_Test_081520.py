From OpenFL import Printer, FLP

p=Printer.Printer()
F=FLP()

while true:
	packets.append(F.LaserPowerLevel(32768))
	packets.append(F.XYMove([[x, y, 60000]]))
	if:
		F.WaitButtonPress()