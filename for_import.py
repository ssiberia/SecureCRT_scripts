
import os
import sys
import logging
import time
import re

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

def check_if_ce(session_name):
	cust_if = ['nhop2','nhop1','CE-2']
	if not [ele for ele in cust_if if(ele in session_name)]:
		return False
	return True

