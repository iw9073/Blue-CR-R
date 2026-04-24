from winrt.windows.devices.enumeration import DeviceUnpairingResultStatus


async def get_paired_devices(devices):
    return [
        d for d in devices
        if d.name and d.pairing and d.pairing.is_paired
    ]


async def unpair_device(device):
    try:
        if not device.pairing.can_unpair:
            return "Cannot unpair"

        result = await device.pairing.unpair_async()

        if result.status == DeviceUnpairingResultStatus.UNPAIRED:
            return "Unpaired successfully"

        elif result.status == DeviceUnpairingResultStatus.ALREADY_UNPAIRED:
            return "Already unpaired"

        else:
            return f"Failed: {result.status}"

    except Exception as e:
        return f"Error: {e}"