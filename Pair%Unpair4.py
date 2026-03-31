import asyncio  # Needed to run asynchronous WinRT calls 
#You must run Python 3.7+ (async support required)
#Install WinRT library first: pip install winrt
from winrt.windows.devices.enumeration import DeviceInformation, DeviceClass

async def list_paired_devices():
    """
    Lists all paired Bluetooth devices.
    """
    try:
        # Get all paired devices
        devices = await DeviceInformation.find_all_async()
        print("All Devices:")
        for d in devices:
            print(f"- {d.name}")
    except Exception as e:
        print(f"Error listing devices: {e}")


async def unpair_device(device_name):
    """
    Automatically unpairs a Bluetooth device by name.
    """
    try:
        # Find all paired devices
        devices = await DeviceInformation.find_all_async()
        found = False

        for d in devices:
            if device_name.lower() in d.name.lower():
                found = True
                print(f"Found device: {d.name}")

                # Check if device has pairing support
                if d.pairing is None:
                    print(f"Device '{d.name}' does not support pairing operations")
                    continue

                # Attempt to unpair
                result = await d.pairing.unpair_async()

                # Check result
                if result.status.value == 0:  # 0 = success
                    print(f"Device '{d.name}' unpaired successfully!")
                else:
                    print(f"Failed to unpair '{d.name}'. Status code: {result.status.value}")

        if not found:
            print(f"No paired device found matching '{device_name}'")

    except Exception as e:
        print(f"Error unpairing device: {e}")


if __name__ == "__main__":
    # Example usage
    device_name = "WH-1000XM4"  # Replace with your device

    # List devices first so you know the exact name
    asyncio.run(list_paired_devices())

    # Unpair the device automatically
    asyncio.run(unpair_device(device_name))