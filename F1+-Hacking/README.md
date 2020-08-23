# This Folder Contains Research Into The Inner Workings of F1+

The two logo files contain the hex code for both the Formlabs boot graphic and the Photonsters boot graphic.

Here is a brief overview of how to use them:
1) Connect an STM Link to the JTAG pins on the motherboard of your F1/F1+
2) Open the ST-Link software and connect to your F1/F1+ using an address of 0x08000000 and size of 0x7FFFF
3) Save your firmware as a .bin file and back it up in case you make a mistake and need to revert to factory firmware settings.
4) Open your firmware with a hex editor (I like HxD)
5) Search the ASCII for the first instance of "spi port" (should be around address 00017580)
6) Leave one "00" byte after the word "port" (70 6F 72 74)
7) Overwrite the next 512 bytes with the image hex
8) Save the .bin file and upload it back onto your F1/F1+
9) Enjoy your new boot image!

You can use any hex bitmap image that is 128 x 32 pixels. It should be exactly 512 bytes.

Similarly, you can change the serial name of your F1/F1+. To find the serial name, search for "machineserial =" (should be somewhere after the 00038000 address); you need to leave the "20" byte between the equals sign and the serial name. You need to make sure that you do not alter the length of the firmware file. If you are using a shorter or longer serial name, offset the difference by adding or removing FF bytes after the 00038CD0 address.

# Grid Table
- The grid table is a 5x5 grid. The lines are spaced 32mm apart, and 0mm X, 0mm Y is in the middle of the build plate: -64, -32, 0, 32, 64 (for each axis).
- The XYCalibrationChecker python script will move the laser spot to each point on the calibration table so you can check whether your calibration needs to be adjusted.
- There currently is no tool for adjusting the table.

# Relevant Formlabs Github Repositories:
- The Maple bootloader is here: [Maple Bootloader](https://github.com/Formlabs/maple-bootloader)
- TinyPrintf is here: [TinyPrintf](https://github.com/Formlabs/tinyprintf)

# Other Relevant Links:
- This Google group figured out how to hack the CTC Riverside (F1+ Clone) to run F1+ firmware: [CTC Riverside Hacking](https://groups.google.com/forum/#!topic/ctc3dprinters/PbFQm_7dXcs%5B1-25%5D)
