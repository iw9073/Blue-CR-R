import asyncio
from winrt.windows.devices.bluetooth import BluetoothLEDevice

async def battery(addr):
    dev = await BluetoothLEDevice.from_bluetooth_address_async(addr)
    if not dev:
        return None # changed from print bc that would only show terminal 

    for s in (await dev.get_gatt_services_async()).services:
        if "180f" in str(s.uuid):  # Battery service
            for c in (await s.get_characteristics_async()).characteristics:
                if "2a19" in str(c.uuid):  # Battery level
                    val = await c.read_value_async()
                    return bytes(val.value)[0]
    return None #changed from print 

if __name__ == "__main__":
    # ask user for bluetooth address
    addr_input = input("enter bluetooth address (no colons, example A1B2C3D4E5F6): ").strip()

    try:
        addr = int(addr_input, 16)  # convert string to int
    except:
        print("invalid address format")
        exit()

    result = asyncio.run(battery(addr))

    if result is not None:
        print(f"battery: {result}%")
    else:
        print("battery not supported or device not found")