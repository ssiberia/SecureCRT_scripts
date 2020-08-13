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
	tmp = CaptureOutputOfCommand("show run | i router bgp|neighbor.*remote-as|address-family ipv[4,6] ", ce_name)
	tmp = remove_line(tmp, ['20570','65300','family'])
	data = '!\r' + tmp + '!\r'
	tmp = CaptureOutputOfCommand("show run | s snmp-server (view|loc|user|group|communi).*", ce_name)
	tmp = remove_line(tmp, ['webmaus'])
	if 'community' in tmp:
		data += tmp + '\r!\r'
	tmp = CaptureOutputOfCommand("show run | s list 6[2-9]", ce_name)
	if 'permit' in tmp:
		data += tmp + '\r!\r'
	tmp = CaptureOutputOfCommand("show run | s flow", ce_name)
	tmp = remove_line(tmp, ['ip flow monitor ',' ip flow ','remark'])
	data += tmp + '\r!\r'
	tmp = CaptureOutputOfCommand("show ip flow interface", ce_name)
	if 'Invalid' not in tmp:
		data += tmp + '\r!\r'
	tmp = CaptureOutputOfCommand("show flow interface", ce_name)
	if 'Invalid' not in tmp:
		tmp = remove_line(tmp, ['traffic(ip)'],['FNF','monitor','direction',':','  '])
		tmp.strip()
		tmp = tmp.replace('FLOW-MONITOR-',' ip flow monitor FLOW-MONITOR-')
		tmp = tmp.replace('\r\nInput',' input')
		tmp = tmp.replace('\r\nOutput',' output')
		data += tmp + '\r!\r'
	data += tmp + '\r!\r'
	tmp = CaptureOutputOfCommand("show run | s nat ", ce_name)
	tmp = remove_line(tmp, [' ip nat inside',' ip nat outside'])
	data += tmp + '\r!\r'
	tmp = CaptureOutputOfCommand("show run | s dhcp", ce_name)
	tmp = remove_line(tmp, ['no service dhcp'])
	data += tmp + '\r!\r'
	tmp = CaptureOutputOfCommand("show ip helper-address", ce_name)
	if 'Unknown' in tmp:
		tmp = remove_line(tmp, ['Helper-Address  VPN VRG Name'],['Unknown','None',' 0 '])
		data += '!Ip helper\r' + tmp + '\r!\r'
	tmp = CaptureOutputOfCommand("show run | s router (eigrp|rip|ospf)", ce_name)
	data += tmp + '\r!\r'
	tmp = CaptureOutputOfCommand("show run | i ip route", ce_name)
	tmp = remove_line(tmp, ['Dialer10','Virtual-PPP','reachability'])
	data += tmp + '\r!\r'
	tmp = CaptureOutputOfCommand("show run | s ROUTES-IN|ROUTES-OUT", ce_name)
	tmp = remove_line(tmp, ['seq 5 deny 0.0.0.0/','seq 1000 permit 0.0.0.','description **** Filter','match ip address'])
	data += tmp + '\r!\r'
	tmp = CaptureOutputOfCommand("show policy-map interface brief", ce_name)
	data += tmp + '\r!\r'
	tmp = CaptureOutputOfCommand("show run | s ded cos", ce_name)
	tmp = remove_line(tmp, ['deny   ip any any'],['ip access-list extended'])
	if 'permit' in tmp:
		data += tmp + '\r!\r'
	tmp = CaptureOutputOfCommand("show access-lists | i Exten|Stand", ce_name)
	tmp = remove_line(tmp, ['61','63','64','67','SEC_QU','AUX-SSH','PROTOCOLS','cos-map-acc','sl_def_acl'])
	if 'IP' in tmp:
		data += '!customer ACL-s\r' + tmp + '\r!\r'
	data = remove_line(data, ['show'])
	crt.Clipboard.Format = "CF_TEXT"
	crt.Clipboard.Text = data

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

