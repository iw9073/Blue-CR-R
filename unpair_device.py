from bluetooth_utils import get_paired_devices, run_async


async def unpair_device(device_name: str):
    try:
        devices = await get_paired_devices()
        matches = [d for d in devices if device_name.lower() in d.name.lower()]

        if not matches:
            print(f"No paired device found matching '{device_name}'")
            return

        for d in matches:
            print(f"Unpairing: {d.name}...")

            result = await d.pairing.unpair_async()

            status = str(result.status)

            if "SUCCESS" in status.upper():
                print(f" Successfully unpaired '{d.name}'")
            else:
                print(f"Failed to unpair '{d.name}' (Status: {status})")

    except Exception as e:
        print(f"Error unpairing device: {e}")


if __name__ == "__main__":
    device_name = input("Enter device name to unpair: ")
    run_async(unpair_device(device_name))