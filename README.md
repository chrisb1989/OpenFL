# Goals
This repository contains an API for interfacing with the Form 1/1+ 3D printer. The goals of this project are:

1) Integrate the Form 1 and Form 1+ with third party open source slicing software to untether us from PreForm 2.3.3
2) Develop a database of third party resin profiles for the Form 1 and Form 1+
3) Test alternative printing techniques for the Form 1+, like vertical peel
4) Test replacement consumables, like third party vats and build plates
5) Test hardware modifications, like laser upgrades, vat wipers, etc.

If you would like to contribute time, consumables (resin, FEP film, vats, build plates, etc.), or hardware to this project, send an email to thelavachemist@gmail.com or open a new Github issue.

# Modules in the OpenFL scripts directory are for Python 2.7
The Python 3 version of OpenFL does not work properly and causes errors with numpy. I'm hoping to find a fix for this soon.

# Windows Executables (experimental but seem to work):
You can try to run the standalone Windows executable versions of the Community Python scripts:
[OpenFL Executables](https://github.com/opensourcemanufacturing/OpenFL/releases/tag/0.1)

Note: You may need to update your USB drivers for the executables to work. Use Zadig to switch your Form1/1+ driver to use LibusbK instead of Winusb. You can find Zadig here: [Zadig](https://zadig.akeo.ie/)

# Summary
OpenFL provides a number of distinct features for doing interesting non-standard things with a Form 1/1+:

1. A special version of PreForm that allows setting of custom material settings: 
   1. custom laser powers
   2. custom laser speeds
   3. custom motor speeds
2. Python bindings for talking with the printer, including reading and writing machine-code ("FLP" files) to/from the printer.
3. A Python API for manipulating FLP files.
4. A special firmware which adds:
   1. a wait-on-pin command to allow a print to pause for outside input
   2. a write-serial command and a write-serial time command to allow logging and to allow the printer to notify other electronics of events

Notes:
* The OpenFL version of PreForm, that allows exposure to be customized, does not require custom firmware or the Python tools.
* The custom PreForm is not required to use the Python tools.
* The custom firmware is required to use the Python printer API.
* The custom firmware is compatible with other versions of PreForm.


# Quickstart
## PreForm
In order to use all of the firmware features and to set custom material files for Form 1/1+, you need a special version of PreForm, available here:
* https://s3.amazonaws.com/FormlabsReleases/Release/2.3.3/PreForm_2.3.3_release_OpenFL_build_2.dmg
* https://s3.amazonaws.com/FormlabsReleases/Release/2.3.3/PreForm_setup_2.3.3_release_OpenFL_build_2.exe

Use that version of PreForm to update the firmware. Next, you can load the custom material file, [Form_1+_FLGPCL02_100.ini](Form_1+_FLGPCL02_100.ini) from the PreForm UI and print with it by selecting the "Load Custom Material..." button:

<img src="LoadCustomMaterial.png" width="500" alt="In the OpenFL version of PreForm, you can select a custom Form 1/1+ material by clicking the &quot;Load Custom Material...&quot; button.">

For more details, see [Material file detailed description](material_file_description.md).

## Python tools
To install dependencies, run
```
pip install -r requirements.txt
```

Then, have a look through the `examples` subfolder.

Advanced FLP commands are documented in [ADVANCED.md](ADVANCED.md)

# Modifying prints
A print can be read from the printer. Each layer is a "block" on the printer, which can be read as a `FLP.Packets` object, which is a Python `list`.

Here's an example interaction with an uploaded print:
```
>>> from OpenFL import Printer, FLP
>>> p=Printer.Printer()
>>> assert 0 in p.list_blocks() # If this fails, then there are no layers on the printer
>>> layer = p.read_block_flp(block=0)
>>> assert isinstance(layer, FLP.Packets)
>>> assert isinstance(layer, list)
>>> layer[:11] # This will be different depending on the print
[<XYMoveClockRate(60000 Hz) at 0x106f41610>,
 <LayerDone() at 0x106f415d0>,
 <ZCurrent(80) at 0x106f41650>,
 <TiltCurrent(80) at 0x106f416d0>,
 <ZFeedRate(4000 usteps/s) at 0x106f41710>,
 <ZMove(2000 usteps) at 0x106f41790>,
 <WaitForMovesToComplete() at 0x106f417d0>,
 <WaitForMovesToComplete() at 0x106f41750>,
 <ZFeedRate(4000 usteps/s) at 0x106f41810>,
 <ZMove(-1960 usteps) at 0x106f41850>,
 <WaitForMovesToComplete() at 0x106f41890>]
>>> print layer[9]
0x03 ZMove -1960
>>> layer[9].usteps
-1960
>>> layer[9].usteps = 42
>>> layer[9]
<ZMove(42 usteps) at 0x106f41850>
```
alternately, you could do:
```
>>> layer[9] = FLP.ZMove(usteps=42) # Overwrite packet
```
or
```
del layer[9] # Delete packet from list
layer.insert(9, FLP.ZMove(usteps=42)) # Insert packet
```
because FLP.Packets is a Python list (i.e., it inherits list) so you can append, insert, concatenate, etc.

Finally, the block can be pushed back to the printer:
```
p.write_block(0, layer)
```

# LEGAL DISCLAIMER
SEE [NOTICE FILE](NOTICE.md).

# Copyright
Copyright 2016-2017 Formlabs

Released under the [Apache License](https://github.com/formlabs/openfl/blob/master/COPYING).
