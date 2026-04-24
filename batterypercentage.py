import asyncio
from winrt.windows.devices.bluetooth import BluetoothLEDevice


async def get_battery(device):
    try:
        device = await BluetoothLEDevice.from_id_async(device.id)
        if not device:
            return None

        services = (await device.get_gatt_services_async()).services

        for s in services:
            # Battery service UUID = 180F
            if "180f" in str(s.uuid).lower():

                chars = (await s.get_characteristics_async()).characteristics

                for c in chars:
                    # Battery level UUID = 2A19
                    if "2a19" in str(c.uuid).lower():
                        val = await c.read_value_async()
                        return bytes(val.value)[0]

        return None

    except Exception as e:
        print(f"Battery error: {e}")
        return None