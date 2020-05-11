
# https://pypi.org/project/ssh2-python/
# https://pypi.org/project/ssh2-python/#complete-example

# %%

from __future__ import print_function

import os
import sys
import socket
import subprocess
import re
import datetime
import getpass

from ssh2.session import Session
import urllib.request

# %%
host = '192.168.112.194'
remote_user = 'root'
myusername = os.getlogin()
privkey_path_win = fr'C:\Users\{os.getlogin()}\.ssh'
# Potential bug with WSL.
#privkey_path_linux = f'/home/{getpass.getuser()}/.ssh/'

privkey_path_linux = f'/home/{myusername}/.ssh/'
privkey_path_osx = r''
privkey_name = 'smart-ip-updater'
#message = 'ls; exit 2'


# %%


def getPublicIP():
    # https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python
    external_ip = urllib.request.urlopen(
        'https://ident.me').read().decode('utf8')
    return external_ip


def getPrivateKeyPath():

    if sys.platform == 'win32':
        privkey_absolute = fr'{privkey_path_win}\{privkey_name}'
        return privkey_absolute

    # if linux
    if sys.platform == 'linux':
        privkey_absolute = f'{privkey_path_linux}/{privkey_name}'
        return privkey_absolute


def getSystemIdentifier():
    # https://stackoverflow.com/questions/2461141/get-a-unique-computer-id-in-python-on-windows-and-linux

    # if windows
    if sys.platform == 'win32':
        unique_id = subprocess.check_output(
            'wmic csproduct get uuid').decode().split('\n')[1].strip()
        return unique_id

    # if linux
    if sys.platform == 'linux':
        f = os.popen('dmidecode | grep -i UUID')
        output = f.read()
        matched = re.match(r'.*UUID:\s+([a-zA-Z0-9\-]+).*', output)
        unique_id = matched.group(1)
        return unique_id

    # Need MAC OSX
    else:

        print('unknown operating  system')
        exit()


class sshConnect:
    def __init__(self, host, username, privkey, message):
        self.host = host
        self.username = username
        self.privkey = privkey
        self.message = message

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, 22))

        session = Session()
        session.handshake(sock)
        session.userauth_publickey_fromfile(
            self.username, self.privkey)

        channel = session.open_session()
        channel.execute(self.message)
        size, data = channel.read()
        while size > 0:
            print(data)
            size, data = channel.read()
        channel.close()
        print("Exit status: %s" % channel.get_exit_status())


public_ip_address = getPublicIP()

system_id = getSystemIdentifier()
print(public_ip_address)

print(getSystemIdentifier())

now = datetime.datetime.now()
current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

message = f'echo "{public_ip_address}, {os.getlogin()}, {current_date_time}, {system_id}" >> test.txt'

print(getPrivateKeyPath())
sshConnect(host, remote_user, getPrivateKeyPath(), message)


# %%


# %%
