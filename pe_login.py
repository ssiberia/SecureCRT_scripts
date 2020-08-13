# $language = "python"
# $interface = "1.0"

import os, re
from time import sleep

text_word = os.environ.get('text_word')
TAB = crt.GetScriptTab()
TAB.Screen.Synchronous = True

def Main():
	session_name = TAB.Session.Path
	# crt.Dialog.MessageBox(session_name)
	if session_name.find('PE') != -1:
		return 0
	TAB.Screen.Send(chr(13))
	ce_name = TAB.Screen.ReadString("#")
	data = CaptureOutputOfCommand("show int desc", ce_name)
	pe_name = re.findall(r"\w\w\w-\D\D\d\d", data)
	if len(pe_name) != 0:
		pe_login(pe_name[0], ce_name)
	else:
		pe_name = re.findall(r"\w\w\w-\w\w\w\d\d\b", data)
		ce_ip = re.findall(r"(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])", data)
		lns_pe_login(pe_name[0], ce_name, ce_ip[0])


def pe_login(pe_name, ce_name = ""):
	crt.Session.ConnectInTab("/s nhop/PE-1")
	tab = crt.GetActiveTab()
	tab.Screen.Synchronous = True
	tab.Screen.WaitForString("$")
	tab.Screen.Send("login " + pe_name + chr(13))
	tab.Screen.WaitForString("Password for akovac32: ")
	tab.Screen.Send(text_word + chr(13))
	tab.Screen.WaitForString(pe_name)
	ce_name = ce_name.lstrip()
	tab.Screen.Send("show int desc | match " + ce_name + chr(13))

def lns_pe_login(pe_name, ce_name = "", ce_ip = 0):
	crt.Session.ConnectInTab("/s nhop/PE-2")
	tab = crt.GetActiveTab()
	tab.Screen.Synchronous = True
	tab.Screen.WaitForString("~]$", 2)
	tab.Screen.Send("login " + pe_name + chr(13))
	tab.Screen.WaitForString("Password for akovac32: ")
	tab.Screen.Send(text_word + chr(13))
	pe_name += "#"
	tab.Screen.WaitForString(pe_name)
	tab.Screen.Send("term mon" + chr(13))
	tab.Screen.WaitForString(pe_name)
	tab.Screen.Send("term len 0" + chr(13))
	tab.Screen.WaitForString(pe_name)
	ce_name = ce_name.lstrip()
	ce_ip = ce_ip.lstrip()
	ce_ip = ce_ip.rstrip()
	tab.Screen.Send("sh run | i " + ce_name + chr(13) + chr(13) + "sh run | i neighbor " + ce_ip + " peer-group" + chr(13))
	tab.Screen.WaitForString(pe_name)
	tab.Screen.Send(chr(13) + "sh use | s " + ce_ip + chr(13))
	tab.Screen.WaitForString(pe_name)

def CaptureOutputOfCommand(command, prompt):
	TAB.Screen.Send(command + '\r')
	return TAB.Screen.ReadString(prompt)

Main()

