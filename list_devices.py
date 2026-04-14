from bluetooth_utils import get_paired_devices, run_async


async def list_paired_devices():
    try:
        devices = await get_paired_devices()

        if not devices:
            print("No paired Bluetooth devices found.")
            return

        print("Paired Bluetooth Devices:")
        for d in devices:
            print(f"- {d.name}")

    except Exception as e:
        print(f"Error listing devices: {e}")


if __name__ == "__main__":
    run_async(list_paired_devices())