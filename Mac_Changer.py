#GOKUL - MAC CHANGER
#!/usr/bin/env python
import subprocess
import optparse
import re

def get_options():
    parse = optparse.OptionParser()
    parse.add_option("-i", "--interface",dest="interface",help="Used to change interface")
    parse.add_option("-m", "--mac",dest="new_mac",help="Used to change mac")
    (options , argument)=parse.parse_args()
    if not options.interface:
        parse.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parse.error("[-] Please specify an mac address, use --help for more info")
    else:
        return options

def mac_changer(interface,new_mac):
    print(" [+]Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["sudo","ifconfig", interface, "down"])
    subprocess.call(["sudo","ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo","ifconfig", interface, "up"])

def get_mac_address(interface):
    # Here we use regex to print out just the MAC address from the result of ifconfig
    ifconfig_result = subprocess.check_output(["ifconfig",interface])
    # '\w' is for alphanumeric digits, written with colon to print our MAC
    filter_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if filter_result:
        return filter_result.group(0)
    else:
        print("[-] Could not read MAC address")


# Main code for macchanger
options = get_options()
mac_address_filter_result = get_mac_address(options.interface)
print(" [+]Current Mac = " + str(mac_address_filter_result))
mac_changer(options.interface, options.new_mac)
mac_address_filter_result= get_mac_address(options.interface)
if mac_address_filter_result == options.new_mac:
    print(" [+]Mac Address changed to:"+mac_address_filter_result)
else:
    print("[-]Mac Address is Not Changed")
