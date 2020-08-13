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
	hsrp = CaptureOutputOfCommand("show standby brief", ce_name)
	hsrp = remove_line(hsrp, ['Interface','indicates'])
	lines = hsrp.split('\r')
	TAB.Screen.Send("conf te" + chr(13))
	for line in lines:
		if 'local' in line:
			if 'Standby' in line:
				TAB.Screen.Send("int " + str(line.split(' ')[0].strip()) + chr(13))
				TAB.Screen.Send("standby" + str(re.findall(r"\W\d{3}", line)[0]) + " preempt delay minimum 3" + chr(13))
				#TAB.Screen.Send("standby " + str(line.split(' ')[1].strip()) + " preempt delay minimum 3" + chr(13))
	if crt.Screen.WaitForString("Standby -> Active", 60) != True:
		TAB.Screen.Send("end" + chr(13))
		return 0
	for line in lines:
		if 'local' in line:
			if 'Standby' in line:
				TAB.Screen.Send("int " + str(line.split(' ')[0].strip()) + chr(13))
				TAB.Screen.Send("standby" + str(re.findall(r"\W\d{3}", line)[0]) + " preempt delay minimum 300" + chr(13))
	TAB.Screen.Send("end" + chr(13))
def CaptureOutputOfCommand(command, prompt):
	TAB.Screen.Send(command + '\r')
	return TAB.Screen.ReadString(prompt)

def remove_line(szoveg, mi_ne, just_words = []):
	lines = szoveg.split('\r')
	szoveg = ""
	for line in lines:
		if len(line.strip())==0:
			continue
		if [ele for ele in just_words if (ele in line)]:
			for i in just_words:
				line = line.replace(i,'')
		if not[ele for ele in mi_ne if (ele in line)]:
			szoveg += line
			szoveg += '\r'
	return szoveg

Main()
