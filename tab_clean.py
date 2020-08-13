# $language = "python"
# $interface = "1.0"

def Main():

	ACTIVE = crt.GetScriptTab()
	i = int(crt.GetTabCount())
	while int(crt.GetTabCount()) != 1:
		TAB = crt.GetTab(i)
		if i == int(ACTIVE.Index):
			i -= 1
			continue
		i -= 1
		TAB.Session.Disconnect()
		TAB.Close()

def CaptureOutputOfCommand(command, prompt):
	TAB.Screen.Send(command + '\r')
	return TAB.Screen.ReadString(prompt)

Main()
