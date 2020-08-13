# $language = "python"
# $interface = "1.0"
'''
File: s:\SecureCRT\precheck.py
Created Date: Monday February 17th 2020
Last Modified: Wednesday February 26th 2020 1:50:19
Author: Attila Kovács
Mail: atka369@gmail.com
-----
Copyright (c) 2020
'''
import time

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
	data = CaptureOutputOfCommand("show int desc", ce_name)
	lines = data.split('\r')
	customer = []
	for line in lines:
		if line.find('ustomer') != -1:
			customer.append(str(line.split(' ')[0]))
	TAB.Screen.Send("conf te" + chr(13))
	for i in customer:
		i = i.lstrip()
		if i.find(".") != -1:
			continue
		TAB.Screen.Send("int " + str(i) + chr(13))
		TAB.Screen.Send("shutdown" + chr(13))
	TAB.Screen.Send("end" + chr(13))

def CaptureOutputOfCommand(command, prompt):
	TAB.Screen.Send(command + '\r')
	return TAB.Screen.ReadString(prompt)

Main()

