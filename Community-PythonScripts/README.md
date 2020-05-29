# Community Python Scripts

* These are experimental. Never run a script you don't understand.
* Read all of the Formlabs OpenFL documentation before beginning. 
* Python 2.7 is recommended, Python 3.8 did not work properly during testing (exception below).
* The ZOffset_V2_Python3.py script is for Python 3. The project is being transitioned to Python 3, so you'll need both versions for now.
* You can use Windows, but it is recommended that you run Linux on a virtual machine (VM) for Python.

# How To Use

1) Read everything in this file, as well as the main [README.md](https://github.com/opensourcemanufacturing/OpenFL/)
2) Install Python 2.7
3) Clone the OpenFL git to the directory of choice on your local computer
4) Install OpenFL - follow the instructions in the main [README.md](https://github.com/opensourcemanufacturing/OpenFL/)
5) Move the script to the OpenFL-master folder
6) Read the script and make sure you understand what it does - there are comments in the scripts that describe how they work
7) Use a terminal or command line to run the script using python
* If the script fails, try power cycling the printer and reseating the USB cable before trying again
* These secripts are experimental and they do occasionally fail, don't be discouraged


# Script Descriptions:

1) [Insertz_100u.py](https://github.com/opensourcemanufacturing/OpenFL/blob/master/Community-PythonScripts/Scripts/Insertz_100u.py)

* This script will allow you to use Z lift for peeling and allow you to disable the tilt peeling. You need to run this script at a 0.1mm layer height with these ["btwnLayerRoutine"](https://github.com/opensourcemanufacturing/OpenFL/blob/master/Community-PythonScripts/VerticalLiftProfile.ini) settings. If you use a different layer height or the wrong "btwnLayerRoutine" the script will not work properly and may crash your printer.
* I recommend deleting all blocks that are currently on your printer before slicing with PreForm. Preform does not delete block numbers when slicing, it overwrites them. So if your current print job is 240 layers tall, and your tallest previous print was 1000 layers tall, the script will run for all 1000 blocks (layers) on your printer. There is a DeleteBlocks.py script that will delete all blocks on the printer (see description below).

* The print restart option in Preform (File > Printers) works if you want to print the same thing more than once.

2) [ZOffset.py](https://github.com/opensourcemanufacturing/OpenFL/blob/master/Community-PythonScripts/Scripts/ZOffset.py)
* Tune your Z offset for the current print without removing your SD card.

3) [DeleteBlocks.py](https://github.com/opensourcemanufacturing/OpenFL/blob/master/Community-PythonScripts/Scripts/DeleteBlocks.py)

* This script will delete all FLP blocks currently on your Form1/1+. This is useful to run before sending a new print job to the printer, particularly if you about to run a script that affects every block on the printer - like the Insertz script.

4) [Z_Jog_052320.py](https://github.com/opensourcemanufacturing/OpenFL/blob/master/Community-PythonScripts/Scripts/Z_Jog_052320.py)
* This script has a GUI. It allows you to move the Z axis in increments of 0.05mm, 0.1mm, 1mm, or 5mm. The script shows your current Z position as a Z offset value in case you want to write it down. The File menu has an option for saving the current Z position as your Z Offset on the SD card in your F1+.
