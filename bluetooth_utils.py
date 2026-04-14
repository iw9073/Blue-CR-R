import sys
import asyncio

# Graceful import handling
try:
    from winrt.windows.devices.enumeration import DeviceInformation, DeviceClass
    WINRT_AVAILABLE = True
except ImportError:
    WINRT_AVAILABLE = False


async def get_all_devices():
    if not WINRT_AVAILABLE:
        raise RuntimeError("WinRT not available. Install with: pip install winrt")

    return await DeviceInformation.find_all_async(DeviceClass.ALL)


async def get_paired_devices():
    devices = await get_all_devices()
    return [d for d in devices if d.pairing.is_paired]


def run_async(coro):
    """
    Safe async runner that works across environments.
    
    """
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)