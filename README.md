# CentriFi

A platform for central management of mesh OpenWRT WiFi access points

README in progress

### INSTALLATION GUIDE

First, make sure you have Python 3.7 or newer installed.
Open the command line (powershell, command prompt, terminal, or the equivalent).
You can check your python version by running the command:

`python -V` or `python --version`

Second, check to see if you have paramiko version 2.7 or newer installed.
You can check this by running the command:

`pip show paramiko`

If paramiko is not found, install it by running the command:

`pip install paramiko`

Then, download the file 'install_script_v2.py' from the setup folder of this repository, navigate to its location within the terminal window, and run it using the command:

`python install_script_v2.py`

First, power on the master access point, and connect it to the internet using an ethernet cable and the WAN port.  Then, connect the access point to your computer (running the install script) using an additional ethernet cable and any of the LAN ports on the device. Wait around 10-15 seconds, or until the lights on the port show a stable connection (if there are lights for the port).

Then, follow the prompts in the terminal window to configure the first (master) access point.

If you have additional access points to configure:
After the first access point has been configured, it will reboot. Once it is finished rebooting, you can disconnect it and connect the next access point to be configured.  Once again, connect the access points WAN port via ethernet to the internet, and then connect it your computer (running the install script) using the additionall ethernet cable and any of the LAN ports on the device.  Again, wait around 10-15 seconds, or until the lights on the port show a stable connection (if there are lights for the port).

Then, continue following the prompts to configure the additional access points.
