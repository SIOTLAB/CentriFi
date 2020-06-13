#   This file is part of CentriFi.
#
#   CentriFi is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   CentriFi is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with CentriFi.  If not, see <https://www.gnu.org/licenses/>.
import subprocess
import pexpect

PROMPT = '[$#]'

print('Depreciated - use install_script_v2.py')
'''
OPKG_PACKAGES_TO_INSTALL = [
    'python3',
    'python3-pip',
    'vnstat',
    'git-http',
    'nmap'
    ]

slave_OPKG_PACKAGES_TO_INSTALL = [
    'vnstat'
]

PIP3_PACKAGES_TO_INSTALL = [
    'pexpect',
    'django'
    ]

UCI_COMMANDS = [
    "uci set dhcp.lan.ra_management='1'",
    "uci set network.lan.gateway='192.168.1.1'",
    "uci add_list network.lan.dns='192.168.1.1'",
    "uci set wireless.radio0.type='mac80211'",
    "uci set wireless.radio0.channel='11a'",
    "uci set wireless.radio0.htmode='VHT80'",
    "uci set wireless.radio0.hwmode='161'",
    "uci set wireless.radio0.disabled='0'",
    "uci set wireless.default_radio0.device='radio0'",
    "uci set wireless.default_radio0.network='lan'",
    "uci set wireless.default_radio0.mode='mesh'",
    "uci set wireless.default_radio0.mesh_id='centrifi'",
    "uci set wireless.default_radio0.encryption='sae'",
    "uci set wireless.default_radio0.key='centrifi'",
    "uci set wireless.default_radio0.mesh_fwding='1'",
    "uci set wireless.default_radio0.mesh_rssi_threshold='0'",
    "uci set wireless.radio1.disabled='0'",
    "uci set wireless.default_radio1.device='radio1'",
    "uci set wireless.default_radio1.network='lan wan wan6'",
    "uci set wireless.default_radio1.mode='ap'",
    "uci set wireless.default_radio1.ssid='OpenWRT'",
    "uci set wireless.default_radio1.encryption='psk2'",
    "uci set wireless.default_radio1.key='centrifi'",
    "uci set wireless.default_radio1.ft_over_ds='1'",
    "uci set wireless.default_radio1.ft_psk_generate_local='1'",
    "uci set wireless.default_radio1.ieee80211r='1'",
    "uci set wireless.default_radio1.disassoc_low_ack='0'",
    "uci commit"
]

INIT_COMMANDS = [
    "vnstat -u -i wlan1 wlan1",
    "vnstat -u -i wlan1 br-lan",
    "/etc/init.d/dnsmasq disable",
    "/etc/init.d/dnsmasq stop",
    "/etc/init.d/odhcpd disable",
    "/etc/init.d/odhcpd stop",
    "/etc/init.d/firewall disable",
    "/etc/init.d/firewall stop",
    "/etc/init.d/vnstat restart"
]

DEVICE_NUMBER = 1

COMMAND = "ifconfig"

ADMIN_PASSWORD = ''

def try_connection():
    """ Tests the connection using subprocess to ssh into the connected device. """
    ssh = subprocess.Popen(["ssh", "root@OpenWRT", COMMAND], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = ssh.stdout.readlines()

    for i, msg in enumerate(output):
        output[i] = msg.decode("utf-8")

    if output == []:
        error = ssh.stderr.readlines()
        for i, msg in enumerate(error):
            error[i] = msg.decode("utf-8")
        for err in error:
            print(err)
            return False
    else:
        print('Connection Successful')
        return True

def configure_ap(typ='slave'):
    """ Configures the access point, of typ 'slave' by default, or typ 'master' through command line pexpect calls. """
    global ADMIN_PASSWORD
    global DEVICE_NUMBER
    print('Device number: ', DEVICE_NUMBER)
    # Open connection to access point
    # On the AP
        # Set root password
        # Update opkg
        # Download necessary packages
        # Download CentriFi from github
        # Edit configuration files
        # Start CentriFi server
    print("Called configure master AP")
    child = pexpect.spawn("ssh -l root 192.168.1.1")
    fout = open("LOG.txt", "wb")
    child.logfile = fout
    i = child.expect(['[Pp]assword: ', PROMPT])

    if i == 0:
        child.sendline('centrifi')

        i = child.expect(['denied', 'incorrect', PROMPT])

        if i in (0, 1):
            print('Error, could not login')
            return
        if i == 2:
            print('Successful login to AP')
    if i == 1:
        print('Success login to AP')

    # SET ROOT PASSWORD
    if ADMIN_PASSWORD == '':
        ADMIN_PASSWORD = input("Please enter your desired admin password: ")

    child.sendline('passwd')
    child.expect('password: ')
    child.sendline(ADMIN_PASSWORD)
    child.expect('password: ')
    child.sendline(ADMIN_PASSWORD)
    child.expect(PROMPT)
    print('Password set.')

    # UPDATE OPKG
    print('Updating opkg, please wait...')
    child.sendline('opkg update')
    child.expect(PROMPT, timeout=300)
    print('opkg updated.')

    # REMOVE WPAD-BASIC, ADD WPAD-MESH
    child.sendline('opkg remove wpad-basic')
    child.expect(PROMPT)
    print('wpad-basic removed.')

    child.sendline('opkg install wpad-mesh')
    child.expect(PROMPT)
    print('wpad-mesh installed.')

    # FIND ATH10K FIRMWARE AND REPLACE WITH NON-CT VERSION
    child.sendline('opkg list-installed')
    child.expect(PROMPT)
    output = child.before.decode("utf-8")
    ath_drv_start = output.find('ath10k-firmware-qca9')
    ath_drv_end = ath_drv_start + output[ath_drv_start:].find('-ct')
    ath_drv = output[ath_drv_start:ath_drv_end]

    if ath_drv == '':
        print('no ath driver found, skipping...')
    else:
        remove_drv = 'opkg remove ' + ath_drv + '-ct'
        child.sendline(remove_drv)
        child.expect(PROMPT)
        print(ath_drv + '-ct' + ' removed.')

        add_drv = 'opkg install ' + ath_drv
        child.sendline(add_drv)
        child.expect(PROMPT)
        print(ath_drv + ' installed.')

    # DOWNLOAD NECESSARY PACKAGES FOR MASTER AP
    if typ == 'master':
        for package in OPKG_PACKAGES_TO_INSTALL:
            command = 'opkg install ' + package
            print(command)
            child.sendline(command)
            child.expect(PROMPT, timeout=300)
            print(package, 'installed.')

        for package in PIP3_PACKAGES_TO_INSTALL:
            command = 'pip3 install ' + package
            print(command)
            child.sendline(command)
            child.expect(PROMPT, timeout=300)
            print(package, 'installed.')

        print('opkg & pip3 packages installed.')

    if typ == 'slave':
        for package in slave_OPKG_PACKAGES_TO_INSTALL:
            command = 'opkg install ' + package
            child.sendline(command)
            child.expect(PROMPT, timeout=300)
            print(package, 'installed.')

    # EDIT CONFIGURATION FILES
    set_ip = "uci set network.lan.ipaddr='192.168.1." + str(DEVICE_NUMBER) + "'"

    child.sendline(set_ip)
    child.expect(PROMPT)
    print(set_ip)

    for command in UCI_COMMANDS:
        child.sendline(command)
        child.expect(PROMPT)
        print(command)
    print('uci commands run.')

    for command in INIT_COMMANDS:
        child.sendline(command)
        child.expect(PROMPT)
        print(command)
    print('init commands run.')

    # IF MASTER AP
    # DOWNLOAD CENTRIFI FROM GITHUB & START CENTRIFI SERVICE
    if typ == 'master':
        child.sendline("git clone https://github.com/AJAnderhub/CentriFi.git")
        i = child.expect(["'https://github.com':", 'Resolving deltas:', PROMPT])
        if i == 0:
            usr = input('GitHub Username: ')
            child.sendline(usr)

            child.expect('Password ')
            psw = input('GitHub Password: ')
            child.sendline(psw)
            child.expect(PROMPT, timeout=300)
            print("CentriFi download from github successful")
        if i == 1:
            child.expect(PROMPT)
            print("CentriFi download (most likely) succesful, check LOG.txt")
        if i == 2:
            print("No need for github login, check LOG.txt")

    if typ == 'master':
        # Start CentriFi server on startup
        child.sendline("sed -i '/nothing./a python3 /root/CentriFi/manage.py runserver 0.0.0.0:8000 &' /etc/rc.local")
        child.expect(PROMPT)

    print('rebooting')
    child.sendline('reboot -d 2')
    child.expect(PROMPT)
    child.sendline('')
    child.sendcontrol('c')
    child.close()
    print(child.exitstatus, child.signalstatus)

    return

def connect_slave_ap():
    """ Manages connecting multiple slave APs """
    global DEVICE_NUMBER
    res = ""
    res = input('Do you have another AP to connect?  (y/n)')
    if res == 'n':
        return
    if res == 'y':
        res = ""
        while res.strip() != "y":
            print('Connect AP via ethernet cable')
            res = input('AP connected? (y/n): ')

        while not try_connection():
            input("Check connection...")

    DEVICE_NUMBER = DEVICE_NUMBER + 1
    configure_ap()
    connect_slave_ap()

def main():
    """ Main functionality, calls to setup the master AP """
    res = ""
    while res.strip() != "y":
        print('Connect Master AP via ethernet cable')
        res = input('AP connected? (y/n): ')

    #while not try_connection():
    #    input("Check connection...")

    # Succesfully connected to Master Access Point
    configure_ap('master')

    connect_slave_ap()

main()
'''
