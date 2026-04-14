from bluetooth_utils import run_async

try:
    from winrt.windows.devices.enumeration import (
        DeviceInformation,
        DevicePairingKinds,
        DevicePairingProtectionLevel
    )
except ImportError:
    raise RuntimeError("WinRT not installed. Run: pip install winrt")


async def pair_device(device_name: str, pin: str = None):
    try:
        devices = await DeviceInformation.find_all_async()

        matches = [d for d in devices if device_name.lower() in d.name.lower()]

        if not matches:
            print(f"No device found matching '{device_name}'")
            return

        for device in matches:
            pairing = device.pairing

            if pairing.is_paired:
                print(f"'{device.name}' is already paired.")
                continue

            print(f"Attempting to pair with: {device.name}")

            custom = pairing.custom

            def pairing_handler(sender, args):
                """
                Handles different pairing scenarios.
                """
                kind = args.pairing_kind

                if kind == DevicePairingKinds.CONFIRM_ONLY:
                    print("Confirming pairing automatically...")
                    args.accept()

                elif kind == DevicePairingKinds.PROVIDE_PIN:
                    user_pin = pin or input("Enter PIN: ")
                    args.accept(user_pin)

                elif kind == DevicePairingKinds.CONFIRM_PIN_MATCH:
                    print(f"Does this PIN match? {args.pin}")
                    confirm = input("Type 'yes' to confirm: ")
                    if confirm.lower() == "yes":
                        args.accept()
                    else:
                        print("Pairing rejected.")

                else:
                    print(f"Unhandled pairing type: {kind}")

            # Attach handler
            custom.add_pairing_requested(pairing_handler)

            result = await custom.pair_async(
                DevicePairingKinds.CONFIRM_ONLY
                | DevicePairingKinds.PROVIDE_PIN
                | DevicePairingKinds.CONFIRM_PIN_MATCH,
                DevicePairingProtectionLevel.DEFAULT
            )

            status = str(result.status)

            if "SUCCESS" in status.upper():
                print(f"Successfully paired with '{device.name}'")
            else:
                print(f"Failed to pair with '{device.name}' (Status: {status})")

            # Cleanup handler
            custom.remove_pairing_requested(pairing_handler)

    except Exception as e:
        print(f"Error pairing device: {e}")


if __name__ == "__main__":
    name = input("Enter device name to pair: ")
    run_async(pair_device(name))