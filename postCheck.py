# $language = "python"
# $interface = "1.0"
'''
File: s:\SecureCRT\postCheck.py
Created Date: Monday February 17th 2020
Last Modified: Wednesday February 26th 2020 1:50:14
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
	TAB.Screen.Clear()
	TAB.Screen.Send(chr(13))
	ce_name = TAB.Screen.ReadString("#")
	ce_name += '#'
	data = ce_name
	vrfek = CaptureOutputOfCommand("show ip vrf", ce_name)
	ifek = CaptureOutputOfCommand("show int desc", ce_name)
	data += vrfek
	data += ifek
	ci_c = CustIf()
	ci_c.first(vrfek,ifek) # kötelező adatgyűjtés van e vrf és az interfacek
	lines = data.split('\r')
	customer = ci_c.get_cust_if() # a customer if-ek kigyűjtése

	for i in customer:	# sh int parancs
		i = i.lstrip()
		if i.find('.') != -1 or i.find('Vl') != -1:
			continue
		tmp_line = "sh int " + i + " | i line|runt|uple|30|packets|CRC|collisions|drops\\b"
		output = CaptureOutputOfCommand(tmp_line, ce_name)
		if (output.find("0 input errors, 0 CRC") == -1) or (output.find("0 output errors, 0 collisions") == -1):
			crt.Dialog.MessageBox(i + " CRC-s vagy erroros!")
		if (output.find("protocol is down") == -1):
			data += ce_name
			data += output
			data += ce_name

	# kiszűrni a szemét vrf-eket
	vrfek = ci_c.get_vrf_only()
	for i in vrfek:
		iface = ci_c.get_cust_if(i)
		if len(iface) == 0:
			vrfek.remove(i)
			continue

	if len(vrfek) == 0:	# sh arp és sh bgp ha NINCS vrf
		arps = CaptureOutputOfCommand("sh arp | e -|Incompl", ce_name)
		if len(arps.split('\r')) > 16:
			arps = split_lines(arps)
		data += arps
		data += ce_name
		bgp = CaptureOutputOfCommand("show ip bgp sum | b N", ce_name)
		lines = bgp.split('\r')
		bgp_nei = ""
		for line in lines:
			if line.find('20570') != -1:
				if line.find('dle') != -1:
					continue
				bgp_nei = str(line.split(' ')[0])
				bgp_nei = bgp_nei.lstrip()
				break
			mi_ne = ['20570','65300','sh ip','BGP','Active','Neighb','show']
			if not [ele for ele in mi_ne if (ele in line)]:
				csali = str(line.split(' ')[0])
				csali = csali.lstrip()
				data += CaptureOutputOfCommand("sh ip bgp nei " + csali + " routes | b N", ce_name)
				data += ce_name
				del csali
		data += bgp
		data += ce_name
		if bgp_nei != '':
			routes = CaptureOutputOfCommand("show ip bgp neig " + bgp_nei + " adv | b N", ce_name)
			if len(routes.split('\r')) > 40:
				routes = split_lines(routes)
			data += routes
		data += ce_name
	else:	# sh arp és sh bgp ha VAN vrf
		for i in vrfek:
			iface = ci_c.get_cust_if(i)
			if len(iface) == 0:
				continue
			for h in iface:
				arps = CaptureOutputOfCommand("sh arp vrf " + str(i) + " " + h +" | e -|Incompl", ce_name)
				if len(arps.split('\r')) > 16:
					arps = split_lines(arps)
				data += arps
				data += ce_name
		for i in vrfek:	# sh bgp
			hellno = CaptureOutputOfCommand("sh ip bgp vpnv4 vrf " + i + " sum | i [1-9]+\.[1-9]+", ce_name)
			bgp_nei = ""
			lines = hellno.split('\r')
			for line in lines:
				if line.find('20570') != -1:
					if (line.find('dle') != -1) or (line.find('ctive') != -1):
						continue
					bgp_nei = str(line.split(' ')[0])
					bgp_nei = bgp_nei.lstrip()
					break
				mi_ne = ['20570','65300','sh ip','BGP','Active','Neighb','show']
				if not [ele for ele in mi_ne if (ele in line)]:
					csali = str(line.split(' ')[0])
					csali = csali.lstrip()
					routes = CaptureOutputOfCommand("sh ip bgp vpnv4 vrf " + i + " nei " + csali + " routes | b N", ce_name)
					if len(routes.split('\r')) > 40:
						routes = split_lines(routes)
					data += routes
					data += ce_name
					del csali
			data += hellno
			data += ce_name
			if bgp_nei != "": # ha nincs nei, akkor csak kiegészítő vrf lesz, kár kiírni
				routes = CaptureOutputOfCommand("sh ip bgp vpnv4 vrf " + i + " nei " + bgp_nei + " adv | b N", ce_name)
				if len(routes.split('\r')) > 40:
					routes = split_lines(routes)
				data += routes
				data += ce_name
	data += CaptureOutputOfCommand("show standby brief", ce_name)
	data += ce_name
	data += CaptureOutputOfCommand("show run | i ! L|! N", ce_name)
	data += ce_name
	data = data.replace("akovac32", "*****", 99)
	data = data.replace("loc_account_04", "*****", 99)
	crt.Clipboard.Format = "CF_TEXT"
	crt.Clipboard.Text = data


def CaptureOutputOfCommand(command, prompt):	# prompt copy to slipboard
	TAB.Screen.Send(command + '\r')
	return TAB.Screen.ReadString(prompt)

class CustIf():
	
	def __init_(self, onlyvrf, onlycustif):
		self.onlyvrf = onlyvrf # ["melyikvrf", ["if1", "if2", "if3"]] # nincs kiszűrve h csak customer if
		self.onlycustif = onlycustif # a customer if-ek listája, a két lista között itt nincs kapcsolat

	def first(self, vrfs, interfaces): # kezdeti inicializálás
		self.onlyvrf = []
		vrfs = re.findall(r"\w\w\w-\d\d\d\d\d\d", vrfs) # vrf RegEx
		if int(len(vrfs)) != 0:
			data = CaptureOutputOfCommand("sh ip vrf interfaces", "#")	#adatgyűjtés
			lines = data.split('\n')
			for i in vrfs:
				ifek = [] # egy adott vrf összes if-e
				for line in lines:
					if str(i) in str(line): # megállapítani az adott if vrf-ét
						interf = line.split(' ')
						ifek.append(interf[0])
				resulttmp = [i,ifek]
				self.onlyvrf.append(resulttmp)	# visszaadunk: ["melyikvrf", ["if1", "if2", "if3"]]
		self.onlycustif = []
		cust_if = ['Fa','Gi','Te','Vl']
		lines = interfaces.split('\r')
		for line in lines:
				if line.find('ustomer') != -1:
					if [ele for ele in cust_if if(ele in line)]:
						self.onlycustif.append(str(line.split(' ')[0]))

	def get_vrf_only(self):	# az összes vrf listáját kidobja
		vrfek = []
		for i in self.onlyvrf:
			vrfek.append(i[0])
		return vrfek # ["vrf1","vrf2","vrf3"] formában
	
	def get_cust_if(self,melyikvrf = ""):  # a stringként megadott vrfhez tartozó customer if lista
		if melyikvrf == "":
			return self.onlycustif # ha 1 vrf van akkor csak 1 vrf-é lehet az összes if ["if1","if2"]
		vrf_cust_if = []
		for i in self.onlyvrf:
			if i[0] == melyikvrf:
				for n in self.onlycustif:
					for h in i[1]: # megnézni h van e egyezés a VRF összes if-e és a cust_if lista között. mivel csak 1 db lehet, instant visszaköpi
						h = h.lstrip()
						h = h.rstrip()
						n = n.lstrip()
						n = n.rstrip()
						if h == n:
							vrf_cust_if.append(h)
		return vrf_cust_if # adott vrf összes if-e ["if1","if2"]...

	def vrf_count(self):
		return int(len(self.onlyvrf))
	
def split_lines(data):
	result = data.split('\r')
	lines = 0
	for i in range(7,len(result)-6):
		result.pop(7)
		lines += 1
	result.insert(7, "\r<.." + str(lines) + ".more.lines..>")
	str1 = ""
	for h in result:
		str1 += h
	return str1

Main()

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
