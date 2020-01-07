import random
import os
import time
import sys

def getInterfaces():
    # Get interfaces using network-manager
    interfaces = os.popen("nmcli device").read()
    # Parse and filter connected interfaces
    interfaces = [i.split()[0] for i in interfaces.split("\n")[1:-1] if i.split()[2] == "connected"]

    return interfaces

def genMac():
    # Generate even 1st octet
    h1 = ((random.randint(0, 128)) * 2 - 2)

    # Generate remaining octets
    h2 = random.randint(0, (16 ** 10) -1)

    # Combines octets to create MAC address
    mac = str(hex(h1 * (16 ** 10) + h2))[2:] 

    return mac

def setMac(interface, mac):
    # Update interface to new MAC
    os.system("ifconfig " + interface + " down")
    os.system("ifconfig " + interface + " hw ether " + mac)
    os.system("ifconfig " + interface + " up")

    print("Updated " + interface + " to " + mac)

# Detect interfaces
interfaces = getInterfaces();

# Update all detected interfaces
for i in interfaces:
    setMac(i, genMac())

# Get interval argv
if len(sys.argv) > 1:
    interval = float(sys.argv[1])
else:
    interval = -1

# Loop if interval is given
while interval > 0:
    time.sleep(interval)
    for i in interfaces:
        setMac(i, genMac())