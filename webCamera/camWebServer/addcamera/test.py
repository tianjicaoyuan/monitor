#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  CameraClient.py
import subprocess
filePath="/home/pi/Documents/test.txt"
ssidname="raspery"
password="123"
subprocess.call('chmod +x /home/pi/Documents/test.sh',shell=True)
p=subprocess.Popen(['/home/pi/Documents/test.sh',ssidname,password],stdout=subprocess.PIPE)
print(p.stdout.read())
