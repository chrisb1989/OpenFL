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
- Deep dive into galvonometers: [Inside the Closed Loop Laser Beam Stearing Galvanometer (YouTube)](https://www.youtube.com/watch?v=HIBH55cbfLM&list=WL&index=38&t=0s)

# OpenOCD Configuration (PiSWD Rev 0.1)

- Installation steps for OpenOCD on your Raspberry Pi (3 or newer):

1) $ sudo apt-get install git autoconf libtool make pkg-config libusb-1.0-0 libusb-1.0-0-dev

2) $ git clone http://openocd.zylin.com/openocd

3) $ cd openocd

4) $ ./bootstrap

5) $ ./configure --enable-sysfsgpio --enable-bcm2835gpio

6) $ make

- Ensure that "/usr/local/share/openocd/scripts/interface" has the following configuration swd pin configuration: bcm2835gpio_swd_nums 25 24

- Use the openocd.cfg file in this repository

- This the pinout for this configuration if you are not using a PiSWD board:

SWDCLK on the F1/F1+ JTAG connector to pin 22 (GPIO 25) on your Raspberry Pi
SWDIO on the F1/F1+ JTAG connector to pin 18 (GPIO 24) on your Raspberry Pi
Ground on the F1/F1+ JTAG connector to pin 6 or pin 9 (ground) on your Raspberry Pi

- Either provide 3.3V to the VCC pin on the F1/F1+ or power the F1/F1+ using the power supply, but never do both at the same time!

- SWDRST is not used, but it is connected on the PiSWD Rev 0.1 board if you need it for some reason.

- To start OpenOCD:
1) install telnet and the telnet daemon:

$ sudo apt-get install telnetd
$ sudo apt-get install telnet

2) run the following command on your Pi: sudo openocd
3) Open a second terminal window, or another SSH session to your Pi and use telnet to connect to your Pi on port 4444: 

$ telnet 127.0.0.1 4444

4) To read read the F1+ configuration to a .bin file called test.bin, run the following command from the openocd command line: 

flash read_bank 0 test.bin (this will save the firmware as test.bin in the OpenOCD directory)

5) Exit the telnet session with the exit command.

- You can then edit your firmware with a hex editor of your choice (hexedit is installed by default).

- We used these links as reference material to set up the configuration, all credit goes to the original authors:

http://openocd.org/doc/html/index.html

https://learn.adafruit.com/programming-microcontrollers-using-openocd-on-raspberry-pi/compiling-openocd

https://iosoft.blog/2019/01/28/raspberry-pi-openocd/ 

https://medium.com/@ly.lee/openocd-on-raspberry-pi-better-with-swd-on-spi-7dea9caeb590