# main page for app 
# instead of running multiple files, user runs this one

import os

print("bluetooth manager")
print("1. battery percentage")
print("2. unpair device")
print("3. list devices")

choice = input("choose option: ")

if choice == "1":
    # runs battery script
    os.system("python \"batterypercentage.py\"") #deprecated system but reliable

elif choice == "2":
    # runs pair/unpair script
    os.system("python \"pairunpair.py\"")

elif choice == "3":
    # runs list devices script
    os.system("python \"list_devices\"")

else:
    print("invalid option")