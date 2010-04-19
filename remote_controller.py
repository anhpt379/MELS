#! /usr/bin/python
#! coding: utf-8
# cd /home/src
# git clone git://github.com/AloneRoad/MELS.git
from lib import ssh

private_key = "id_rsa"
remote = ssh.Connection('203.128.246.60', 'root', private_key)
print remote.execute("ps xa | grep python")