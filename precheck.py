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
	TAB.Screen.Clear()
	TAB.Screen.Send(chr(13))
	ce_name = TAB.Screen.ReadString("#")
	ce_name += '#'
	data = ce_name
	data = data[2:]
	data += CaptureOutputOfCommand("show ip vrf", ce_name)
	data += ce_name
	data += CaptureOutputOfCommand("show int desc", ce_name)
	data += ce_name
	data += CaptureOutputOfCommand("show ip int brief", ce_name)
	data += ce_name
	lines = data.split('\r')
	customer = []
	for line in lines:
		if (line.find('ustomer') != -1) and (line.find('admin down') != -1):
			customer.append(str(line.split(' ')[0]))
	data += CaptureOutputOfCommand("sh run | s list (63|64)", ce_name)
	data += ce_name
	routing = CaptureOutputOfCommand("sh run | s router (eigrp|rip|ospf)", ce_name)
	if routing.find("router ") != -1:
		try:
			crt.Dialog.MessageBox(str(routing.split('\r')[1]) + " implemented! Be careful!")
		except:
			pass
	data += routing
	data += ce_name
	bgp = CaptureOutputOfCommand("show run | i router bgp|neighbor.*remote-as", ce_name)
	ases = bgp.split('\r')
	ases.pop(0)
	for i in ases:
		if (i.find("20570") == -1) and (i.find("65300") == -1):
				crt.Dialog.MessageBox("BGP in LAN! Be careful!")
	data += bgp
	del ases
	data += ce_name
	data += CaptureOutputOfCommand("sh run | s ip route", ce_name)
	data += ce_name
	data += CaptureOutputOfCommand("sh run | s ip help", ce_name)
	data += ce_name
	dhcp = CaptureOutputOfCommand("sh run | s dhcp", ce_name)
	if dhcp.find("ip dhcp ") != -1:
			crt.Dialog.MessageBox("DHCP implemented! Be careful!")
	data += dhcp
	data += ce_name
	nat = CaptureOutputOfCommand("sh run | s nat ", ce_name)
	if nat.find("ip nat") != -1:
			crt.Dialog.MessageBox("NAT implemented! Be careful!")
	data += nat
	data += ce_name
	del nat
	for i in customer:
		data += ce_name
		i = i.lstrip()
		shint = CaptureOutputOfCommand('sh run int '+i, ce_name)
		data += shint
		ip = ''
		vrf = ''
		lines = shint.split('\r')
		for i in lines:
			if 'vrf forw' in i:
				vrf = str(i.split(' ')[4])
			if 'no ip add' in i:
				continue
			if 'ip address ' in i:
				ip = str(i.split(' ')[3])
			if ('standby' in i) and ('ip' in i):
				ip = str(i.split(' ')[4])
		if ip != '':
			if vrf != '':
				tmp_line = 'sh ip route vrf ' + vrf + ' ' + ip
				data += CaptureOutputOfCommand('sh ip route vrf ' + vrf + ' ' + ip, ce_name)
			else:
				data += CaptureOutputOfCommand('sh ip route ' + ip, ce_name)
			#crt.Dialog.MessageBox(vrf + ' ' + ip)
	data += ce_name
	data2 = "conf te\n"
	for i in customer:
		i = i.lstrip()
		if i.find("Vl") != -1:
			tmp_line = "no spanning-tree Vlan " + i[2:] + "\n"
			data2 += tmp_line
	for i in customer:
		i = i.lstrip()
		tmp_line = "interface " + i + "\n no shut\n"
		data2 += tmp_line
	data2 += "end"
	crt.Clipboard.Format = "CF_TEXT"
	crt.Clipboard.Text = data2
	time.sleep(0.3)
	crt.Clipboard.Format = "CF_TEXT"
	crt.Clipboard.Text = data


def CaptureOutputOfCommand(command, prompt):
	TAB.Screen.Send(command + '\r')
	return TAB.Screen.ReadString(prompt)

def remove_line(szoveg, mi_ne):
	# removes a line from a multi line string, which contains one of the forbibben words
	lines = szoveg.split('\r')
	szoveg = ""
	for line in lines:
		if len(line.strip())==0:
			continue
		if not[ele for ele in mi_ne if (ele in line)]:
			szoveg += line
			szoveg += '\r'
	return szoveg

Main()

