﻿#coding=utf-8
import os
import time
import sys
import subprocess
"""
监听WVS扫描
"""
while not os.path.exists('result.txt'):
	time.sleep(20)
	print 'listen ......'
print 'starting  wvs scan'

popen = subprocess.Popen("cmd.exe /c" + "wvs.bat", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while True:
	next_line = popen.stdout.readline()
	if next_line == '' and popen.poll() != None:
		break
	sys.stdout.write(next_line)