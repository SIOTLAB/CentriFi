import os
import subprocess
import platform
import sys
import ast

command = "ifconfig"

def intro_message():
    print("Make sure you have the git commandline tool installed.")

def connect_master_ap():
    print('Connect Master AP')
    return input('AP connected? (y/n): ')

def try_connection():
    ssh = subprocess.Popen(["ssh", "root@OpenWRT", command],
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    output = ssh.stdout.readlines()

    for i, x in enumerate(output):
        output[i] = x.decode("utf-8")

    if output == []:
        error = ssh.stderr.readlines()
        for i, x in enumerate(error):
            error[i] = x.decode("utf-8")
        for x in error:
            print(x)

        return 0
    else:
        for x in output:
            print(x, end='')
        return 1

def main():
    u_res = "";

    while(u_res.strip() != "y"):
       u_res = connect_master_ap()

    while not try_connection():
        input("Check connection...")
