# $language = "python"
# $interface = "1.0"

'''
File: c:\Users\H85714952\Documents\Scripts\SecureCRT python\login.py
Created Date: Monday February 17th 2020
Last Modified: Monday March 2nd 2020 10:16:3
Author: Attila Kovács
Mail: atka369@gmail.com
-----
Copyright (c) 2020
'''

import os, re
from collections import OrderedDict

text_word = os.environ.get('text_word')

def Main():
	# objTab = crt.GetScriptTab()
	# objConfig = objTab.Session.Config
	# session_name = objTab.Session.Path
	# crt.Dialog.MessageBox(session_name)
	router_names = crt.Clipboard.Text
	ces = re.findall(r"\w{2}-\w{3}-\w{4,}-\w{2}-\d{2}", router_names) # vrf RegEx
	if len(ces) == 0:
		return 0
	ces = list(OrderedDict.fromkeys(ces)) # remove list duplicates
	objTab = crt.GetScriptTab()
	session_name = objTab.Session.Path
	cust_if = ['nhop2','nhop1','CE-2']
	if not [ele for ele in cust_if if(ele in session_name)]:
		return 0
	del session_name
	TAB1 = crt.GetScriptTab()
	TAB1.Screen.Synchronous = True
	ce_login(TAB1, ces[0])
	ces.pop(0)
	if len(ces) != 0:
		for ce in ces:
			crt.Session.ConnectInTab("/s nhop/CE-2")
			TAB2 = crt.GetActiveTab()
			TAB2.Screen.Synchronous = True
			TAB2.Screen.WaitForString("akovac32")
			ce_login(TAB2, ce)

def ce_login(tab, ce_name):
	tab.Screen.Send(chr(13))
	siker = tab.Screen.ReadString(['#','$'])
	if '@' not in siker:
		if '(conf' in siker:
			tab.Screen.Send('end' + chr(13))
		tab.Screen.Send('exit' + chr(13))
		crt.Screen.WaitForString('$')
	tab.Screen.Send("login " + str(ce_name) + chr(13))
	tab.Screen.WaitForString("Password for akovac32: ")
	tab.Screen.Send(text_word + chr(13))
	ce_name += "#"
	tab.Screen.WaitForString(ce_name,5)
	tab.Screen.Send("term mon\nterm len 0\nsh ip vrf\nsh int desc\n")
	tab.Screen.WaitForString("Interface")

def CaptureOutputOfCommand(TAB, command, prompt):
	TAB.Screen.Send(command + '\r')
	return TAB.Screen.ReadString(prompt)

Main()

