
# https://pypi.org/project/ssh2-python/
# https://pypi.org/project/ssh2-python/#complete-example

# %%

from __future__ import print_function

import os
import sys
import socket
import subprocess
import re

from ssh2.session import Session
import urllib.request

# %%
host = '192.168.112.193'
remote_user = 'root'
privkey = r'C:/Users/seanryan/.ssh/ssh-python-test'
#message = 'ls; exit 2'


# %%


def getPublicIP():
    # https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python
    external_ip = urllib.request.urlopen(
        'https://ident.me').read().decode('utf8')
    return external_ip


def getSystemIdentifier():
    # https://stackoverflow.com/questions/2461141/get-a-unique-computer-id-in-python-on-windows-and-linux

    operating_system = sys.platform

    # if windows
    if operating_system == 'win32':
        unique_id = subprocess.check_output(
            'wmic csproduct get uuid').decode().split('\n')[1].strip()
        return unique_id

    # if linux
    if operating_system == 'linux':
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

local_user = os.getlogin()

message = f'echo "{public_ip_address}, {local_user}, {system_id}" >> test.txt'
sshConnect(host, remote_user, privkey, message)


# %%


# %%
