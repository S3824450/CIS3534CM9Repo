#!/usr/bin/env python3
# Jeremy McHenry
# McHenry_GPA_8.py
# 7/21/2025
# M8 GPA 8

# Try/except clause for importing JSON
try:
    import json
except ImportError:
    print("Error: JSON module could not be imported.")
    exit()

# File constants
ROUTER_FILE = "equip_r.txt"
SWITCH_FILE = "equip_s.txt"
UPDATED_FILE = "updated.txt"
ERROR_FILE = "errors.txt"

# Prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

# Function to get valid device
def getValidDevice(routers, switches):
    while True:
        device = input(UPDATE + QUIT).lower()
        if device in routers or device in switches or device == 'x':
            return device
        else:
            print("That device is not in the network inventory.")

# Function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    while True:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        if len(octets) != 4:
            invalidIPCount += 1
            invalidIPAddresses.append(ipAddress)
            print(SORRY)
            continue
        try:
            if all(0 <= int(byte) <= 255 for byte in octets):
                return ipAddress, invalidIPCount
            else:
                raise ValueError
        except ValueError:
            invalidIPCount += 1
            invalidIPAddresses.append(ipAddress)
            print(SORRY)

def main():
    # Read JSON files into dictionaries
    try:
        with open(ROUTER_FILE, 'r') as file:
            routers = json.load(file)
        with open(SWITCH_FILE, 'r') as file:
            switches = json.load(file)
    except Exception as e:
        print(f"Error reading input files: {e}")
        return

    updated = {}
    invalidIPAddresses = []
    devicesUpdatedCount = 0
    invalidIPCount = 0
    quitNow = False

    # Display network inventory
    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items():
        print(f"\t{router}\t\t{ipa}")
    for switch, ipa in switches.items():
        print(f"\t{switch}\t\t{ipa}")

    while not quitNow:
        device = getValidDevice(routers, switches)
        if device == 'x':
            break

        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)

        if device in routers:
            routers[device] = ipAddress
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        updated[device] = ipAddress

        print(f"{device} was updated; the new IP address is {ipAddress}")

    # Summary
    print("\nSummary:\n")
    print("Number of devices updated:", devicesUpdatedCount)

    # Write updated dictionary
    try:
        with open(UPDATED_FILE, 'w') as file:
            json.dump(updated, file)
        print(f"Updated equipment written to file '{UPDATED_FILE}'")
    except Exception as e:
        print(f"Error writing to {UPDATED_FILE}: {e}")

    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    # Write invalid IPs
    try:
        with open(ERROR_FILE, 'w') as file:
            json.dump(invalidIPAddresses, file)
        print(f"List of invalid addresses written to file '{ERROR_FILE}'")
    except Exception as e:
        print(f"Error writing to {ERROR_FILE}: {e}")

if __name__ == "__main__":
    main()



