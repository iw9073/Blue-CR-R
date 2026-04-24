import asyncio
from winrt.windows.devices.enumeration import DeviceInformation


async def get_devices():
    devices = await DeviceInformation.find_all_async()

    clean_devices = []

    for d in devices:
        # Must have a name
        if not d.name:
            continue

        # OPTIONAL FILTER (you can remove this if it hides devices)
        if (
            "BluetoothDevice_" not in d.id
            and "Dev_" not in d.id
        ):
            continue

        # Avoid duplicates
        if any(existing.id.split("_")[1:2] == d.id.split("_")[1:2] for existing in clean_devices):
            continue

        clean_devices.append(d)

    return clean_devices