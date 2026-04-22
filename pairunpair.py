import asyncio
import platform  # used to check what operating system is running
import logging   # used to track events instead of just printing

from winrt.windows.devices.enumeration import DeviceInformation, DeviceClass


# this makes sure the program only runs on windows
# winrt bluetooth functions do not work on mac or linux
if platform.system() != "Windows":
    print("this app only works on windows")
    exit()


# basic logging setup 
logging.basicConfig(level=logging.INFO)

async def list_paired_devices():
    """
    gets all paired bluetooth devices and shows them to the user
    we return the list so we can use it later instead of asking again
    """
    try:
        # lists all bluetooth audio/video devices 
        devices = await DeviceInformation.find_all_async(DeviceClass.ALL)

        logging.info("finding paired bluetooth devices...")  
        # using logging instead of print

        print("paired bluetooth devices:")

        # we number them so the user can pick one easily instead of typing the name
        filtered_devices = []

        for d in devices:
            # filter only bluetooth devices that have names
            if d.name and "Bluetooth" in str(d.id):
                filtered_devices.append(d)

        print("paired bluetooth devices:")

        for i, d in enumerate(filtered_devices):
            print(f"{i+1}. {d.name}")

        return filtered_devices

        return devices  # returning this lets us reuse the same list later

    except Exception as e:
        # if something goes wrong, we show the error so we know what happened
        print(f"error listing devices: {e}")
        return []  # return empty list so program doesn’t crash


async def unpair(device):
    """
    unpairs the selected bluetooth device
    we pass the actual device instead of the name to avoid matching issues
    """
    #  try more than once in case bluetooth fails the first time
    for attempt in range(2):
        try:
            result = await device.pairing.unpair_async()

            if result.status == 0:
                logging.info(f"successfully unpaired {device.name}")  
                # logs success so we know it worked without relying only on print

                return True
            else:
                logging.warning(f"failed to unpair {device.name}, status: {result.status.value}")  
                # logs failure with status code for debugging

        except Exception as e:
            logging.error(f"error during unpair attempt {attempt+1}: {e}")  
            # logs error details instead of just printing

    return False


if __name__ == "__main__":

    # shows lists of all devices
    devices = asyncio.run(list_paired_devices())

    # if no devices  found, stops program
    if not devices:
        exit()

    # ask user to choose a device by number
    choice = input("\nselect device #: ")

    # make sure the input is actually a number
    if not choice.isdigit():
        print("bad input")
        exit()

    idx = int(choice) - 1  # convert to index (lists start at 0)

    # check if the number is within range
    if idx < 0 or idx >= len(devices):
        print("out of range")
        exit()

    # get the actual device the user selected
    selected_device = devices[idx]

    # call the unpair function on that device
    success = asyncio.run(unpair(selected_device))

    # show result to user
    if success:
        print(f"unpaired '{selected_device.name}' successfully!")
    else:
        print("error when upairing device.")