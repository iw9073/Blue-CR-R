import asyncio  # Needed to run asynchronous WinRT calls
# Requires Python 3.7+
# Install WinRT: pip install winrt

from winrt.windows.devices.enumeration import DeviceInformation, DeviceClass


async def list_paired_devices():
    """
    Lists all paired Bluetooth devices.
    """
    try:
        # Use ALL instead of AUDIO_VIDEO (fix)
        devices = await DeviceInformation.find_all_async(DeviceClass.ALL)

        print("Paired Bluetooth Devices:")
        for d in devices:
            if d.pairing.is_paired:  # Only show paired devices
                print(f"- {d.name}")

    except Exception as e:
        print(f"Error listing devices: {e}")


async def unpair_device(device_name):
    """
    Automatically unpairs a Bluetooth device by name.
    """
    try:
        # Use ALL instead of AUDIO_VIDEO (fix)
        devices = await DeviceInformation.find_all_async(DeviceClass.ALL)
        found = False

        for d in devices:
            # Only check paired devices
            if d.pairing.is_paired and device_name.lower() in d.name.lower():
                found = True
                print(f"Found device: {d.name}")

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
    device_name = "Your Headphones Name"  # Replace with your device

    # List devices first so you know the exact name
    asyncio.run(list_paired_devices())

    # Unpair the device automatically
    asyncio.run(unpair_device(device_name))