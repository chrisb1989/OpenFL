On Lubuntu/Ubuntu (probably other distros too), you can fix the annoying lack of USB user rights for the Form1/1+.

1) Place the .rules file into the following directory: /etc/udev/rules.d
2) Issue these commands in terminal: 
  $ sudo udevadm control --reload
  $ sudo udevadm trigger
3) Unplug/replug your Form1/1+
4) No more need for sudo in order to run OpenFL scrips!
