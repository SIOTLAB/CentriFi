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
