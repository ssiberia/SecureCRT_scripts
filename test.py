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
	word = CaptureOutputOfCommand("", "show run | i ! L|! N")
	crt.Clipboard.Format = "CF_TEXT"
	crt.Clipboard.Text = word
	
	
def CaptureOutputOfCommand(command, prompt):
	TAB.Screen.Send(command + '\r')
	return TAB.Screen.ReadString(prompt)

Main()
