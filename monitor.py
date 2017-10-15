"""

Simple Monitor Mode script
 - Enables monitor mode on specified interface
 - Disables monitor mode on specified interface

TO DISABLE MONITOR MODE: monitor.py --stop

Coded by Mitchell Wolfe
10/14/17

"""
import sys
import subprocess

def monON(interfaceToMon):
        global airmon_output
	airmon_output = subprocess.check_output("airmon-ng start " + interfaceToMon, shell=True)

def monOFF(inter):
	global airmon_output_off
	airmon_output_off = subprocess.check_output("airmon-ng stop " + inter, shell=True)

if(len(sys.argv) > 1):
	if(sys.argv[1] == "--stop"):
		ifconfig_output_off = subprocess.check_output("ifconfig", shell=True)
		isOn = False
		for row in ifconfig_output_off.split("\n"):
			if "mon" in row:
				isOn = True
				offMonInterface = row.split(":")[0]

				print("Stopping " + offMonInterface)
				monOFF(offMonInterface)
				for row in airmon_output_off.split("\n"):
					if "station" in row:
						stationInterface = row.split("]")[1].split(")")[0]
						print("Stationed mode enabled on " + stationInterface)
		if(isOn == False):
			print("Monitor mode is not enabled")


	else:
		print("To stop monitor mode: " + sys.argv[0] + " --stop")

else:
	interface_list = []
	hasInterface = False
	output = subprocess.check_output("ifconfig", shell=True)
	for row in output.split("\n"):
		if ": flags" in row:
			interfacetmp = row.split(": flags")
			if "eth" not in interfacetmp[0] and "lo" not in interfacetmp[0]:
				interface_list.append(interfacetmp[0])
				hasInterface = True
	if(hasInterface):
		x = 0
		while(x < len(interface_list)):
			print("["+ str(x) + "]     " + interface_list[x])
			x+=1
		choose_interface = input("Select interface: ")
		interface = interface_list[choose_interface]
		
		monON(interface)
		
		for row in airmon_output.split("\n"):
			if "monitor mode vif enabled" in row:
				temp_monInterface = row.split("on [phy")
				temp2_monInterface = temp_monInterface[1].split("]")
				temp3_monInterface = temp2_monInterface[1].split(")")
				global monInterface
				monInterface = temp3_monInterface[0]
		
		
		print(monInterface)
	else:
		print("No wireless interfaces detected")

