
# https://pypi.org/project/ssh2-python/
# https://pypi.org/project/ssh2-python/#complete-example

from __future__ import print_function

import os
import socket

from ssh2.session import Session

host = '192.168.112.193'
user = 'root'
privkey = r'C:/Users/seanryan/.ssh/ssh-python-test'
message = 'ls; exit 2'


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
