# $language = "python"
# $interface = "1.0"
'''
File: s:\SecureCRT\op_delete.py
Created Date: Monday February 17th 2020
Last Modified: Wednesday February 26th 2020 1:51:23
Author: Attila Kovács
Mail: atka369@gmail.com
-----
Copyright (c) 2020
'''

import re

TAB = crt.GetScriptTab()
TAB.Screen.Synchronous = True

def Main():
	session_name = TAB.Session.Path
	cust_if = ['nhopbb','PE-1']
	if not [ele for ele in cust_if if(ele in session_name)]:
		return 0
	if_name = crt.Clipboard.Text
	if '/' not in if_name:
		return 0
	if_name = if_name.lstrip()
	data = CaptureOutputOfCommand("show configuration interfaces " + if_name + chr(13), "master")
	vrf_name = re.findall(r"\w\w\w-\d\d\d\d\d\d", data)
	TAB.Screen.Send("op delete-vrf-intf vrf " + vrf_name[0] + " interface " + if_name + chr(13))

def CaptureOutputOfCommand(command, prompt):
	TAB.Screen.Send(command + '\r')
	return TAB.Screen.ReadString(prompt)

Main()
