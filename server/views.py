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
import re
import ast
import json
import pexpect
import threading
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseServerError
from django.shortcuts import render

# Create your views here.
ACCESS_POINT_LIST = []
PASSWORD = ''
PROMPT = '[$#]'

def index(request):
    return render(request, 'server/index.html', {})

# POST Request
# Check if sent login password matches root password
def login(request):
    global PASSWORD
    global PROMPT

    print(request)
    password = json.loads(request.body)['password']

    check = pexpect.spawn("login root")
    check.expect('[Pp]assword: ')
    check.sendline(password)

    i = check.expect(['incorrect', PROMPT])

    if i == 0:
        print('ERROR: Incorrect Password')
        check.sendcontrol('d')
        return HttpResponseForbidden()

    if i == 1:
        data = {'Accepted':'Accepted'}
        print('Correct Password')
        check.sendline('exit')

        PASSWORD = password
        return JsonResponse(data)
        #return HttpResponse('Accepted', status=200)

    return HttpResponseServerError()

def update_network_info(request):
    wifi_name = pexpect.run('uci get wireless.default_radio1.ssid')
    wifi_name = wifi_name.decode("utf-8").strip()

    mesh_key = pexpect.run('uci get wireless.default_radio0.key')
    mesh_key = mesh_key.decode("utf-8").strip()

    net_inf = pexpect.run('nmap -sn --send-ip 192.168.1.0-31')
    net_inf = net_inf.decode("utf-8")
    print(net_inf)

    ip_list = re.findall(r'[0-9]+(?:\.[0-9]+){3}', net_inf)
    mac_list = re.findall(r'[a-fA-F0-9:]{17}|[a-fA-F0-9]{12}', net_inf)
    name_list = []

    for mac in mac_list:
        name_list.append(net_inf[net_inf.find(mac) + len(mac) + 2:net_inf.find(')', net_inf.find(mac))])

    hostname = pexpect.run('uci get system.@system[0].hostname').decode("utf-8").strip()
    ip = pexpect.run('uci get network.lan.ipaddr').decode("utf-8").strip()

    mac_addr = pexpect.run('ifconfig br-lan').decode("utf-8")
    mac_addr = mac_addr[mac_addr.find('HWaddr ') + 7:mac_addr.find('HWaddr ') + 24]

    ip_list.insert(0, ip)
    mac_list.insert(0, mac_addr)
    name_list.insert(0, hostname)

    aps = []
    for ip, mac, name in zip(ip_list, mac_list, name_list):
        temp = {}
        temp['apIP'] = ip
        temp['apMAC'] = mac
        temp['apType'] = name
        aps.append(temp)

    data = {}
    data['wifiName'] = wifi_name
    data['meshKey'] = mesh_key
    data['aps'] = aps

    global ACCESS_POINT_LIST

    if ACCESS_POINT_LIST != aps:
        print("ACCESS POINT LIST UPDATED")
        ACCESS_POINT_LIST = aps

    with open('network_info.dat', 'w+') as fp:
        fp.write(json.dumps(data))

    return data

# GET Request
# Return APs on the network & WiFi Settings
def list_network_info(request):
    print(request)

    try:
        print("NETWORK INFO FROM FILE")
        with open('network_info.dat', 'r') as fp:
            data = json.loads(fp.read())
            thread = threading.Thread(target=update_network_info, args=[request])
            thread.start()
            return JsonResponse(data)

    except FileNotFoundError:
        print("UPDATE NETWORK INFO CALLED")
        data = update_network_info(request)
        return JsonResponse(data)

# POST Request
# Set passwords for all devices on the network
def set_router_passwords(request):
    global ACCESS_POINT_LIST
    global PASSWORD
    global PROMPT

    ips = []
    for ap in ACCESS_POINT_LIST:
        ips.append(ap["apIP"])

    print(request)

    new_pass = json.loads(request.body)['newPassword']
    old_pass = json.loads(request.body)['currPassword']

    if PASSWORD != old_pass:
        print('Incorrect current password')
        return HttpResponseForbidden()

    for ip in ips:
        command = "ssh -l root " + ip
        child = pexpect.spawn(command)
        i = child.expect(['password: ', '(y/n)'])
        if i == 1:
            child.sendline('y')
            child.expect('password: ')
        child.sendline(old_pass)

        child.expect(PROMPT)
        child.sendline("passwd")

        child.expect("New password: ")
        child.sendline(new_pass)

        child.expect("Retype password: ")
        child.sendline(new_pass)

        child.expect("password for root changed by root")
        child.close()

    PASSWORD = new_pass

    data = {'Accepted':'Accepted'}
    return JsonResponse(data)

# GET Request
# Return detailed WiFi Settings
def get_wifi_settings(request):
    global ACCESS_POINT_LIST
    global PROMPT

    print(request)

    ssid = pexpect.run('uci get wireless.default_radio1.ssid')
    ssid = ssid.decode("utf-8").strip()
    print(ssid)

    key = pexpect.run('uci get wireless.default_radio1.key')
    key = key.decode("utf-8").strip()
    print(key)

    aps = []
    for ap in ACCESS_POINT_LIST:
        login_cmd = "ssh -l root " + ap["apIP"]
        child = pexpect.spawn(login_cmd)

        i = child.expect(['password: ', '(y/n)'])
        print(child.before.decode('utf-8'))

        if i == 1:
            child.sendline('y')
            child.expect('password: ')
        child.sendline(PASSWORD)

        child.expect(PROMPT)
        child.sendline('uci get wireless.radio1.channel')

        child.expect(PROMPT)
        output = child.before.decode("utf-8").strip()
        output_list = [str(s) for s in output.split() if s.isdigit()]

        if output_list:
            channel = output_list[0]
        else:
            channel = ''

        print('Channel:', channel)

        temp = {}
        temp['apIP'] = ap["apIP"]
        temp['channel'] = channel

        aps.append(temp)

    encryption = pexpect.run('uci get wireless.default_radio1.encryption')
    encryption = encryption.decode("utf-8").strip()
    print(encryption)

    if encryption == 'psk2':
        security = 'WPA2'
    elif encryption == 'sae':
        security = 'WPA3'
    else:
        security = 'UNSURE'
    print(security)

    data = {
        'networkName': ssid,
        'password': key,
        'security': security,
        'aps': aps
    }

    print(ACCESS_POINT_LIST)

    return JsonResponse(data)

# POST Request
# Set new WiFi settings
def set_wifi_settings(request):
    global ACCESS_POINT_LIST
    global PASSWORD
    global PROMPT

    print(request)
    print(request.body)

    net_name = json.loads(request.body)['networkName']
    password = json.loads(request.body)['password']
    security = json.loads(request.body)['security']
    aps = json.loads(request.body)['aps']

    print(net_name)
    print(password)
    print(security)
    print(aps)

    set_name = "uci set wireless.default_radio1.ssid=" + "\'" + net_name + "\'"
    set_pass = "uci set wireless.default_radio1.key=" + "\'" + password + "\'"

    if security == 'WPA2':
        set_security_1 = "uci set wireless.default_radio1.encryption='psk2'"
        set_security_2 = "uci delete wireless.default_radio1.ieee80211w"
    elif security == 'WPA3':
        set_security_1 = "uci set wireless.default_radio1.encryption='sae'"
        set_security_2 = "uci set wireless.default_radio1.ieee80211w='2'"

    ips = []
    channels = []
    for ap in aps:
        ips.append(ap['apIP'])
        channels.append(ap['channel'])

    for ip, channel in zip(ips, channels):
        set_channel = "uci set wireless.radio1.channel=" + "\'" + channel + "\'"

        login_cmd = "ssh -l root " + ip
        child = pexpect.spawn(login_cmd)
        i = child.expect(['password: ', '(y/n)'])
        if i == 1:
            child.sendline('y')
            child.expect('password: ')
        child.sendline(PASSWORD)

        child.expect(PROMPT)
        child.sendline(set_name)

        child.expect(PROMPT)
        child.sendline(set_pass)

        child.expect(PROMPT)
        child.sendline(set_channel)

        child.expect(PROMPT)
        child.sendline(set_security_1)

        child.expect(PROMPT)
        child.sendline(set_security_2)

        child.expect(PROMPT)
        child.sendline("uci commit")

        child.expect(PROMPT)
        child.sendline("wifi up")

        child.close()

    data = {
        'networkName': net_name,
        'password': password,
        'security': security,
        'aps': aps
    }

    return JsonResponse(data)

# GET Request
# Send vnstat data for each router on the network
def network_statistics(request):
    global ACCESS_POINT_LIST
    global PASSWORD
    global PROMPT

    print(request)

    ips = []
    for ap in ACCESS_POINT_LIST:
        ips.append(ap["apIP"])

    outputs = []

    for ip in ips:
        login_cmd = "ssh -l root " + ip
        child = pexpect.spawn(login_cmd, encoding='utf-8')
        i = child.expect(['password: ', '(y/n)'])
        if i == 1:
            child.sendline('y')
            child.expect('password: ')
        child.sendline(PASSWORD)

        child.expect(PROMPT)
        child.sendline("vnstat --json")

        child.expect(PROMPT)
        output = child.before

        child.close()

        output = output[output.find('{') : output.rfind('}') + 1]

        if len(output) > 5:
            outputs.append(output)


    data = {}
    stat_list = []

    for ip, stat in zip(ips, outputs):
        temp = {}
        temp['routerIP'] = ip
        temp['rawVnstat'] = ast.literal_eval(stat)
        stat_list.append(temp)

    data['routerStats'] = stat_list

    print(data)
    return JsonResponse(data)

# GET Request
# Sends list of end devices
def list_end_devices(request):
    global ACCESS_POINT_LIST
    global PASSWORD

    print(request)

    dhcp_list = pexpect.run("cat /tmp/dhcp.leases").decode("utf-8").splitlines()

    device_list = []
    for dev in dhcp_list:
        temp = {}
        device_info = dev.split()

        temp['deviceIP'] = device_info[2]
        temp['deviceName'] = device_info[3]
        temp['deviceMAC'] = device_info[1]
        device_list.append(temp)

    data = {}
    data["devices"] = device_list

    try:
        with open('device_roaming.dat', 'r+') as fp:
            lines = fp.read()
            for device in device_list:
                print(device)
                mac = device['deviceMAC']

                if lines.find(mac) != -1:
                    start = lines.find(mac) + len(mac) + 1
                    substr = lines[start:]
                    end = substr.find('\n')
                    rr_val = lines[start:start+end]
                    device['roamingRestricted'] = rr_val
                else:
                    device['roamingRestricted'] = 'no'
                    fp.write(device['deviceMAC'] + ' ' + device['roamingRestricted'] + '\n')

    except IOError as err:
        with open('device_roaming.dat', 'w') as fp:
            for device in device_list:
                device['roamingRestricted'] = 'no'
                fp.write(device['deviceMAC'] + ' ' + device['roamingRestricted'] + '\n')
            print('File written')

    data["devices"] = device_list
    print(data)

    return JsonResponse(data)

# GET Request
# Set end device to roaming or not roaming
def set_end_devices(request):
    global ACCESS_POINT_LIST
    global PASSWORD
    global PROMPT

    print(request)
    print(request.body)

    # RELEVANT UCI COMMANDS
    set_mac_filter = "uci set wireless.default_radio1.macfilter='deny'"
    add_filter = "uci add_list wireless.default_radio1.maclist="
    del_filter = "uci del_list wireless.default_radio1.maclist="

    device_list = json.loads(request.body)['devices']

    with open('device_roaming.dat', 'w') as fp:
        for device in device_list:
            fp.write(device['deviceMAC'] + ' ' + device['roamingRestricted'] + '\n')

    allowed_ip = ''
    for device in device_list:
        for ap in ACCESS_POINT_LIST:
            remove_from_filter = del_filter + "'" + device['deviceMAC'].upper() + "'"
            allowed_ip = device['roamingRestricted']

            ap_ip = ap['apIP']

            print('configuring ' + ap_ip)
            login_cmd = "ssh -l root " + ap_ip
            child = pexpect.spawn(login_cmd)
            i = child.expect(['password: ', '(y/n)'])
            if i == 1:
                child.sendline('y')
                child.expect('password: ')
            child.sendline(PASSWORD)

            child.expect(PROMPT)
            child.sendline(set_mac_filter)
            print('mac filter set')

            if device['roamingRestricted'] == 'no':
                child.expect(PROMPT)
                child.sendline(remove_from_filter)
                print('removed from filter')

            else:
                if allowed_ip == ap_ip:
                    child.expect(PROMPT)
                    child.sendline(remove_from_filter)
                    print('removed from filter')
                else:
                    add_cmd = add_filter + "'" + device['deviceMAC'].upper() + "'"
                    child.expect(PROMPT)
                    child.sendline(add_cmd)
                    print('added to filter')

            child.expect(PROMPT)
            child.sendline("uci commit")

            disassoc_cmd = 'hostapd_cli disassociate ' + device['deviceMAC'].upper()
            child.expect(PROMPT)
            child.sendline(disassoc_cmd)

            child.expect(PROMPT)
            child.sendline("wifi reload")

            child.close()
            print(ap_ip + ' configured')

    data = {}
    data = json.loads(request.body)

    return JsonResponse(data)

# FUNCTION TO RUN AT STARTUP FROM APPS.PY
def del_ssh_keys():
    pexpect.run('rm /.ssh/known_hosts')
    pexpect.run('rm /root/.ssh/known_hosts')
    print("SSH KNOWN HOSTS DELETED")
