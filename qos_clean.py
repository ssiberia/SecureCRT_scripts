# $language = "python"
# $interface = "1.0"

'''
File: s:\SecureCRT\clean.py
Created Date: Tuesday February 25th 2020
Last Modified: Wednesday February 26th 2020 1:50:5
Author: Attila Kovács
Mail: atka369@gmail.com
-----
Copyright (c) 2020
'''

import re

TAB = crt.GetScriptTab()
TAB.Screen.Synchronous = True

def Main():
	objTab = crt.GetScriptTab()
	session_name = objTab.Session.Path
	cust_if = ['nhop2','nhop1','CE-2']
	if not [ele for ele in cust_if if(ele in session_name)]:
		return 0
	TAB.Screen.Send(chr(13))
	ce_name = TAB.Screen.ReadString("#")
	ce_name += '#'
	baszo = CaptureOutputOfCommand("show run | i policy-map|class-map|ip.access.*cos|ded LOCAL_PROTOCOLS|ROUTES-IN desc|ROUTES-OUT desc|LAN2BGP deny|BGP2LAN deny", ce_name)
	baszo += CaptureOutputOfCommand("", ce_name)
	lines = baszo.split("\r")
	del baszo, ce_name
	lines.pop(0)
	eredmeny = []
	for line in lines:
		if "show" in line:
			continue
		elif "policy-map" in line:
			eredmeny.insert(0, line)
		elif "description" in line:
			line = line.split(" desc")[0]
			eredmeny.append(line)
		elif "deny" in line:
			line = line.split(" deny")[0]
			eredmeny.append(line)
		else:
			eredmeny.append(line)
	del lines
	str1 = ""
	for h in eredmeny:
		k = 'no ' + h[1:]
		str1 += k + "\r"
	crt.Clipboard.Format = "CF_TEXT"
	crt.Clipboard.Text = str1
	
	
def CaptureOutputOfCommand(command, prompt):
	TAB.Screen.Send(command + '\r')
	return TAB.Screen.ReadString(prompt)

Main()


