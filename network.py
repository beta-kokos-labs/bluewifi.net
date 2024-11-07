import time
import bluetooth
from bleak import BleakClient, BleakScanner
import socket

# 1. Basic Bluetooth SPP Connection with PyBluez
def connect_to_bluetooth_device(device_name):
    # Search for nearby Bluetooth devices with the given name
    nearby_devices = bluetooth.discover_devices(lookup_names=True, lookup_oui=True, lookup_oui=True)
    target_device = None

    # Iterate over discovered devices to find one matching the target name
    for addr, name in nearby_devices:
        if device_name.lower() in name.lower():
            target_device = addr
            print(f"Found Bluetooth device: {name} ({addr})")
            break

    if not target_device:
        print("Device not found.")
        return None

    # Connect to the target device using RFCOMM (Serial Port Profile)
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((target_device, 1))  # Connect to the first RFCOMM port
    return sock


# 2. BLE (Bluetooth Low Energy) connection with Bleak
async def connect_to_ble_device(device_name):
    # Scan for BLE devices
    devices = await BleakScanner.discover()
    target_device = None

    # Find device by name
    for device in devices:
        if device_name.lower() in device.name.lower():
            target_device = device
            print(f"Found BLE device: {device.name} ({device.address})")
            break

    if not target_device:
        print("BLE Device not found.")
        return None

    # Connect to the found BLE device
    async with BleakClient(target_device.address) as client:
        print("Connected to BLE device!")
        return client


# 3. Data sending function for SPP (via PyBluez RFCOMM)
def send_data_spp(sock, data):
    sock.send(data)
    print("Data sent:", data)


# 4. Data sending function for BLE (using Bleak)
async def send_data_ble(client, data):
    await client.write_gatt_char("characteristic_uuid", data.encode('utf-8'))
    print("Data sent via BLE:", data)


# 5. Main function to automatically connect and send data
async def main():
    device_name = "My Bluetooth Device"  # Replace with your target Bluetooth device name
    data = "Hello, Bluetooth world!"

    # First, try to connect using SPP (Classic Bluetooth)
    print("Attempting to connect via Classic Bluetooth (SPP)...")
    sock = connect_to_bluetooth_device(device_name)
    if sock:
        send_data_spp(sock, data)
        sock.close()

    # If Classic Bluetooth connection fails, try BLE connection
    else:
        print("Attempting to connect via BLE...")
        ble_client = await connect_to_ble_device(device_name)
        if ble_client:
            await send_data_ble(ble_client, data)


if __name__ == '__main__':
    # Run the main function asynchronously for BLE communication
    import asyncio
    asyncio.run(main())
