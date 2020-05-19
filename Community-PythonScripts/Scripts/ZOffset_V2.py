# -*- coding: utf-8 -*-

import usb.core
import usb.util


VID = 0x16d0
PID = 0x07eb

# Endpoint numbers for TX and RX

TX_EP = 0x81    # Printer -> computer
RX_EP = 0x03    # Computer -> printer
SOF = 0xFF  # Special character marking the beginning of a transmission
EOF = 0xFE  # Special character marking the end of a transmission
ESCAPE = 0xFD   # Character used to escape special characters in a bytestring
WRITEFILE = 0x63

dev = usb.core.find(idVendor=VID, idProduct=PID)
if dev is None:
	raise ValueError('F1+ is not connected')

dev.set_configuration()

#This section sets the read and write parameters for USB communication, according to the settings above

def writeUSB(data):
	return dev.write(RX_EP, data, timeout=None)
def readUSB(buffsize=1024):
	return dev.read(TX_EP, buffsize, timeout=10000)


'''	This loop asks the user for a Z Offset value, then it updates the user.ini file on the Form1+ SD card via USB.
	If you press Enter at the prompt without giving an offset value, your ZOffset is unchanged.
	If you give the script a 
'''

x = 0
while x == 0:
        ZOffset = raw_input("Enter Z Offset OR Press Enter to Skip:")
        try:
                if ZOffset != "":
                	float(ZOffset) # makes sure you provided a number.
                	inText = bytearray("c   /user.ini")
                	blankSpace = bytearray(118)
                	outText1 = bytearray("s0[serializerSettings]\n\rzOffset="+str(ZOffset)+"\n\r\n\r\n\r[userSettings]\n\rxOffset=0\n\rxScale3=1\n\ryOffset=0\n\ryScale3=1\n\r")
                	payload = bytearray([SOF, WRITEFILE])
                	payload.extend(inText)
                	payload.extend(blankSpace)
                	payload.extend(outText1)
                	payload.append(EOF)
                	print ("saving Z Offset to printer")
                	writeUSB(payload)
                	readUSB()
                        x = 1
                else:
                        x = 1
        except ValueError:
                print ("You must enter a number or press Enter to continue")
                continue



