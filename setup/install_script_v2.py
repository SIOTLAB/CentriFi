import time
import string
import random
from contextlib import suppress
import getpass
import paramiko

IP = '192.168.1.1'
PORT = 22
USERNAME = 'root'
PROMPT = 'root@OpenWrt:~#'

CHANNEL_LIST = ['1', '6', '11']

MASTER_OPKG_PACKAGES_TO_INSTALL = [
    'python3',
    'python3-pip',
    'vnstat',
    'git-http',
    'nmap',
    'hostapd-utils'
    ]

SLAVE_OPKG_PACKAGES_TO_INSTALL = [
    'vnstat',
    'hostapd-utils'
]

MASTER_PIP3_PACKAGES_TO_INSTALL = [
    'pexpect',
    'django'
    ]

SLAVE_UCI_COMMANDS = [
    "uci set dhcp.lan.ra_management='1'",
    "uci set network.lan.gateway='192.168.1.1'",
    "uci add_list network.lan.dns='192.168.1.1'",
    "uci set network.wan.ifname='eth1'"
]

UCI_COMMANDS = [
    "uci set wireless.radio0.type='mac80211'",
    "uci set wireless.radio0.channel='161'",
    "uci set wireless.radio0.htmode='VHT80'",
    "uci set wireless.radio0.hwmode='11a'",
    "uci set wireless.radio0.disabled='0'",
    "uci set wireless.default_radio0.device='radio0'",
    "uci set wireless.default_radio0.network='lan'",
    "uci set wireless.default_radio0.mode='mesh'",
    "uci set wireless.default_radio0.mesh_id='centrifi_mesh'",
    "uci set wireless.default_radio0.encryption='sae'",
    "uci set wireless.default_radio0.mesh_fwding='1'",
    "uci set wireless.default_radio0.mesh_rssi_threshold='0'",
    "uci set wireless.radio1.disabled='0'",
    "uci set wireless.default_radio1.device='radio1'",
    "uci set wireless.default_radio1.network='lan wan wan6'",
    "uci set wireless.default_radio1.mode='ap'",
    "uci set wireless.default_radio1.ssid='CentriFi'",
    "uci set wireless.default_radio1.encryption='psk2'",
    "uci set wireless.default_radio1.key='centrifi'",
    "uci set wireless.default_radio1.ft_over_ds='1'",
    "uci set wireless.default_radio1.ft_psk_generate_local='1'",
    "uci set wireless.default_radio1.ieee80211r='1'",
    "uci set wireless.default_radio1.disassoc_low_ack='0'",
    "uci commit"
]

SLAVE_INIT_COMMANDS = [
    "/etc/init.d/dnsmasq disable",
    "/etc/init.d/dnsmasq stop",
    "/etc/init.d/odhcpd disable",
    "/etc/init.d/odhcpd stop",
    "/etc/init.d/firewall disable",
    "/etc/init.d/firewall stop",
]

MASTER_INIT_COMMANDS = [
]

ADMIN_PASSWORD = ''
CONF_PASSWORD = ''
MESH_PASSWORD = ''

def generate_mesh_password():
    """Generate the password used by the mesh network."""
    contents = string.ascii_letters + string.digits
    return ''.join((random.choice(contents) for i in range(16)))

def set_admin_password(client):
    """Set the admin password on the device connected to by the client."""
    global ADMIN_PASSWORD
    conf_password = 'default password'

    if ADMIN_PASSWORD == '':
        while ADMIN_PASSWORD != conf_password:
            ADMIN_PASSWORD = getpass.getpass("Enter your desired admin password: ")
            conf_password = getpass.getpass("Confirm password: ")
            if ADMIN_PASSWORD != conf_password:
                print("Passwords do not match...")

    channel = client.invoke_shell()

    # CLEAR SHELL OPENING TEXT
    time.sleep(1)
    channel.recv(4096)
    channel.send("\n")
    time.sleep(1)

    # SEND PASSWD COMMAND
    print("Setting admin password.")

    output = ''
    channel.send("passwd\n")
    while 'password:' not in output:
        output = ''
        while not channel.recv_ready():
            time.sleep(0.5)
        time.sleep(0.5)
        output = channel.recv(4096).decode('utf-8')

    channel.send(ADMIN_PASSWORD + '\n')
    channel.recv(4096)

    while 'Retype password:' not in output:
        output = ''
        while not channel.recv_ready():
            time.sleep(0.5)
        time.sleep(0.5)
        output = channel.recv(4096).decode('utf-8')

    channel.send(ADMIN_PASSWORD + '\n')
    time.sleep(1)
    output = channel.recv(4096).decode('utf-8')
    output = output.replace(PROMPT, '')

    print(output)

    channel.close()

def update_opkg(client):
    """Update opkg on the device connected to by the client."""
    stdin, stdout, stderr = client.exec_command('opkg update', get_pty=True)
    for line in iter(stdout.readline, ""):
        print(line, end="")
    print('opkg updated.')

def swap_wpad(client):
    """Replace wpad-basic with wpad-mesh on the device connected to by the client."""
    stdin, stdout, stderr = client.exec_command('opkg remove wpad-basic', get_pty=True)
    for line in iter(stdout.readline, ""):
        print(line, end="")
    print('wpad-basic removed.')

    stdin, stdout, stderr = client.exec_command('opkg install wpad-mesh', get_pty=True)
    for line in iter(stdout.readline, ""):
        print(line, end="")
    print('wpad-mesh installed.')

def swap_ath10k_firmware(client):
    """
    Remove the ath10k-ct firmware from the connected device and replace with the non-ct version.

    The Candela Technologies (-ct) firmware did not work for setting up the mesh network.
    If the ath10k-ct firmware is not found, do nohting.

    """
    stdin, stdout, stderr = client.exec_command('opkg list-installed')
    output = stdout.read().decode('utf-8')
    #print(output)

    ath_drv_start = output.find('ath10k-firmware-qca9')
    ath_drv_end = ath_drv_start + output[ath_drv_start:].find('-ct')
    ath_drv = output[ath_drv_start:ath_drv_end]

    if ath_drv == '':
        print('No ath10k driver found, skipping...')
    else:
        rmv_cmd = 'opkg remove ' + ath_drv + '-ct'
        stdin, stdout, stderr = client.exec_command(rmv_cmd)
        output = stdout.read().decode('utf-8')
        print(output)

        inst_cmd = 'opkg install ' + ath_drv
        stdin, stdout, stderr = client.exec_command(inst_cmd)
        output = stdout.read().decode('utf-8')
        print(output)
        print('ath10k drivers swapped.')

def install_master_opkg_packages(client):
    """Install the necessary opkg packages for the master AP on the connected device."""
    for package in MASTER_OPKG_PACKAGES_TO_INSTALL:
        cmd = 'opkg install ' + package
        stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")

def install_master_pip_packages(client):
    """Install the necessary pip3 packages for the master AP connected to by the client."""
    for package in MASTER_PIP3_PACKAGES_TO_INSTALL:
        cmd = 'pip3 install ' + package
        stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")

def install_slave_opkg_packages(client):
    """Install the necessary opkg packages for the slave APs on the connected device."""
    for package in SLAVE_OPKG_PACKAGES_TO_INSTALL:
        cmd = 'opkg install ' + package
        stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")

def config_mesh(client, type_, ap_num):
    """Run the UCI commands necessary for configuring the mesh network on the connected device."""

    if type_ == 'slave':
        set_ip = "uci set network.lan.ipaddr='192.168.1." + str(ap_num) + "'"
        stdin, stdout, stderr = client.exec_command(set_ip)
        output = stdout.read().decode('utf-8')
        print(set_ip, '\n', output)

        for cmd in SLAVE_UCI_COMMANDS:
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode('utf-8')
            print(cmd, '\n', output)

    # SET MESH PASSWORD
    mesh_pass_cmd = "uci set wireless.default_radio0.key='" + MESH_PASSWORD + "'"
    stdin, stdout, stderr = client.exec_command(mesh_pass_cmd)
    output = stdout.read().decode('utf-8')
    print(mesh_pass_cmd, '\n', output)

    # SET CHANNEL FOR ACCESS POINT
    curr_channel = CHANNEL_LIST.pop()
    set_channel = "uci set wireless.radio1.channel=" + "\'" + curr_channel + "\'"
    CHANNEL_LIST.insert(0, curr_channel)
    stdin, stdout, stderr = client.exec_command(set_channel)
    output = stdout.read().decode('utf-8')
    print(set_channel, '\n', output)

    for cmd in UCI_COMMANDS:
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read().decode('utf-8')
        print(cmd, '\n', output)

def init_slave(client):
    """Run the system service commands necessary for initializing the Slave APs."""
    for cmd in SLAVE_INIT_COMMANDS:
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read().decode('utf-8')
        print(cmd, '\n', output)

def init_master(client):
    """Run the system service commands necessary for initializing the Master AP."""
    for cmd in MASTER_INIT_COMMANDS:
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read().decode('utf-8')
        print(cmd, '\n', output)

def download_centrifi(client):
    """Download the files for CentriFi on the device connected to by the client using git."""
    channel = client.invoke_shell()

    # CLEAR SHELL OPENING TEXT
    time.sleep(1)
    channel.recv(4096)
    channel.send("\n")
    time.sleep(1)

    channel.send("git clone https://github.com/SIOTLAB/CentriFi.git" + '\n')
    time.sleep(1)

    output = channel.recv(1024).decode('utf-8')
    time.sleep(0.5)

    output = channel.recv(1024).decode('utf-8')
    print('working...')

    for i in range(50):
        time.sleep(0.5)
        output = channel.recv(1024).decode('utf-8')
        if PROMPT in output:
            output = output.replace(PROMPT, '')
            print(output)
            break
        else:
            print(output)

    print('done.')
    channel.close()

def del_ssh_keys(client):
    stdin, stdout, stderr = client.exec_command("rm /root/.ssh/known_hosts")
    print('SSH keys removed')

def reboot_ap(client):
    """Reboot the AP connected to by the client."""
    print('rebooting')
    cmd = 'reboot -d 2'
    stdin, stdout, stderr = client.exec_command(cmd)
    output = stdout.read().decode('utf-8')
    print(output)

def set_master_autorun(client):
    """Set the CentriFi django server to autorun on bootup on the connected device."""
    cmd_centrifi = "sed -i '/nothing./a python3 /root/CentriFi/manage.py runserver 0.0.0.0:8000 &' /etc/rc.local"

    cmd_vnstat = "sed -i '/&/a"
    cmd_vnstat += "ntpd -q -p 1.openwrt.pool.ntp.org &"
    cmd_vnstat += r"\nsleep 10 && vnstat -u -i wlan1 &"
    cmd_vnstat += r"\nsleep 10 && vnstat -u -i br-lan &"
    cmd_vnstat += "' /etc/rc.local"

    stdin, stdout, stderr = client.exec_command(cmd_centrifi)
    output = stdout.read().decode('utf-8')
    print(cmd_centrifi, '\n', output)

    stdin, stdout, stderr = client.exec_command(cmd_vnstat)
    output = stdout.read().decode('utf-8')
    print(cmd_vnstat, '\n', output)

def set_slave_autorun(client):
    """Set autorun commands for the slave routers."""
    cmd_vnstat = "sed -i '/nothing./a"
    cmd_vnstat += "ntpd -q -p 1.openwrt.pool.ntp.org &"
    cmd_vnstat += r"\nsleep 10 && vnstat -u -i wlan1 &"
    cmd_vnstat += r"\nsleep 10 && vnstat -u -i br-lan &"
    cmd_vnstat += "' /etc/rc.local"

    stdin, stdout, stderr = client.exec_command(cmd_vnstat)
    output = stdout.read().decode('utf-8')
    print(cmd_vnstat, '\n', output)

def configure_ap(type_, ap_num):
    """Configure the AP of type type_ (master or slave) and number ap_num."""

    print("Configuring", type_, "AP", ap_num)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    with suppress(paramiko.ssh_exception.AuthenticationException):
        client.connect(hostname=IP, username=USERNAME, port=PORT, password='')
    client.get_transport().auth_none(USERNAME)

    set_admin_password(client)
    update_opkg(client)
    swap_wpad(client)
    swap_ath10k_firmware(client)

    if type_ == 'master':
        install_master_opkg_packages(client)
        install_master_pip_packages(client)
        download_centrifi(client)
    else:
        install_slave_opkg_packages(client)

    config_mesh(client, type_, ap_num)

    if type_ == 'master':
        init_master(client)
        set_master_autorun(client)
    else:
        init_slave(client)
        set_slave_autorun(client)

    del_ssh_keys(client)
    reboot_ap(client)
    client.close()

def main():
    """Start the process of installing CentriFi and configuring necessary files."""
    global MESH_PASSWORD

    MESH_PASSWORD = generate_mesh_password()

    print('Connect Master AP via ethernet cable.')
    user_input = ''
    ap_num = 1

    while user_input != 'y':
        user_input = input('Connected?  (y/n): ')

    while user_input == 'y':
        try:
            configure_ap('master', ap_num)
            break
        except TimeoutError as error:
            print('TimeoutError: Connection Attempt Failed')
            print(error)
            print('Check connection...')
            user_input = input('(y to retry connection, anything else to exit program): ')
            if user_input != 'y':
                return

    print("If you have another AP to connect, swap the ethernet cable over now.")
    print("If you do not have another AP to connect, select 'n'.")
    user_input = input('AP connected? (y/n): ')
    ap_num = ap_num + 1
    while user_input == 'y':
        try:
            print("Attempting connection...please wait...")
            time.sleep(15)
            configure_ap('slave', ap_num)
            print("If you have another AP to connect, swap the ethernet cable over now.")
            print("If you do not have another AP to connect, select 'n'.")
            user_input = input('AP connected? (y/n): ')
            ap_num = ap_num + 1
        except TimeoutError as error:
            print('TimeoutError: Connection Attempt Failed')
            print('Check connection...')
            user_input = input('(y to retry connection, anything else to exit program): ')
            if user_input != 'y':
                return

    print("Done with configuration.  Exiting.")

main()
