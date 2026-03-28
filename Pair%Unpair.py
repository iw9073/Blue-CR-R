import subprocess  # Import the subprocess module so we can run PowerShell commands from Python

def pair_device(device_name):
    """
    Pairs a Bluetooth device by name.
    """
    try:
        # Prepare the PowerShell command to pair the device
        # Add-BluetoothDevice is a PowerShell command that pairs a device by its name
        cmd = f'powershell "Add-BluetoothDevice -Name \\"{device_name}\\""'

        # Run the PowerShell command using subprocess
        # shell=True allows running the command in the system shell
        # capture_output=True saves the output so we can check if it worked
        # text=True makes the output readable as text instead of bytes
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:  # returncode 0 means success
            print(f"Device '{device_name}' paired successfully.")
        else:  # If returncode is not 0, there was an error
            print(f"Failed to pair device '{device_name}': {result.stderr}")
    except Exception as e:  # Catch any unexpected errors
        print(f"Error: {e}")


def unpair_device(device_name):
    """
    Unpairs a Bluetooth device by name.
    """
    try:
        # Prepare the PowerShell command to unpair the device
        # Remove-BluetoothDevice is a PowerShell command that removes a paired device by name
        cmd = f'powershell "Remove-BluetoothDevice -Name \\"{device_name}\\""'

        # Run the PowerShell command
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            print(f"Device '{device_name}' unpaired successfully.")
        else:  # If returncode is not 0, print the error message from PowerShell
            print(f"Failed to unpair device '{device_name}': {result.stderr}")
    except Exception as e:  # Catch any unexpected errors
        print(f"Error: {e}")


# Example usage
if __name__ == "__main__":
    device_name = "Your Headphones Name"  # Replace with the name of your Bluetooth device
    pair_device(device_name)       # Call the function to pair the device
    # unpair_device(device_name)   # Call the function to unpair the device (commented out for now)