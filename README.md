# CentriFi

CentriFi is an access point management system that makes creating robust and customizable networks realistic and affordable.  Built on the free OpenWRT platform, CentriFi allows for local area networks to be exactly configured and maintained on low cost hardware, intuitively and easily.

Currently CentriFi sets up a mesh network automatically via an install script. 

From there, CentriFi can be further configured via a web inteface, where the following settings can currently be configured:
- The CentriFi admin password that gives access to configuration
- The SSID, set the password, and the set the security settings (WPA2/WPA3) of the client wifi network
- The radio channel for the client wifi network of each router on the network.
- Whether client devices should be allowed to roam from router to router or be restricted to connect to one specific router on the network

This web interface also allows users to view statistics about the network bandwidth being used by the network as a whole or by each router in the network.

To see a demo of the system, go to this link:

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

Once you have configured all of the access points, you can then move them around to set up the mesh network within the location you want to set up the mesh. The master access point needs to be connected to ethernet and power, the slave access points just need to be connected to power.

Once they are set up and powered on, wait 1-2 minutes and they should be up and running the mesh.

To configure the devices further, and look at the settings, connect to the network 'CentriFi' with password 'centrifi'.

Then, on that device, in a web browser's address bar, visit 192.168.1.1 and you should see the CentriFi homepage.

There is a demo video of the system linked above that should help with any questions regarding further configuration.
