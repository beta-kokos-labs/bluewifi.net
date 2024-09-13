!pip install bluepy
from bluepy.btle import Peripheral, UUID, Service, Characteristic
from bluepy.btle import DefaultDelegate

# Define UUIDs
SERVICE_UUID = UUID("12345678-1234-5678-1234-56789abcdef0")
CHARACTERISTIC_UUID = UUID("abcdef01-2345-6789-abcd-ef0123456789")

class MyDelegate(DefaultDelegate):
    def __init__(self, periph):
        DefaultDelegate.__init__(self)
        self.peripheral = periph

    def handleNotification(self, cHandle, data):
        print("Received notification:", data.decode('utf-8'))

# Create a BLE Peripheral
peripheral = Peripheral()

# Add service and characteristic
service = peripheral.addService(SERVICE_UUID, True)
characteristic = service.addCharacteristic(CHARACTERISTIC_UUID, 
                                            Characteristic.PROP_READ | 
                                            Characteristic.PROP_WRITE, 
                                            Characteristic.PERM_READ | 
                                            Characteristic.PERM_WRITE)

# Set a custom name
peripheral.setName("MyCustomBLEServer")

# Start advertising
peripheral.advertiseService(SERVICE_UUID)

print("Advertising as 'MyCustomBLEServer'...")

# Run the server
try:
    while True:
        if peripheral.waitForNotifications(1.0):
            # Handle notifications
            continue
        print("Waiting for notifications...")
finally:
    peripheral.disconnect()
    print("Disconnected.")

##################################
!pip install bleak
import asyncio
from bleak import BleakScanner, BleakClient

async def run_client():
    print("Scanning for devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name == "MyCustomBLEServer":
            print(f"Found device: {device.name} with address: {device.address}")
            async with BleakClient(device) as client:
                print(f"Connected: {client.is_connected}")

                while True:
                    message = input("Enter message to send: ")
                    if message.lower() == 'exit':
                        break

                    # Write message to the characteristic
                    await client.write_gatt_char(CHARACTERISTIC_UUID, message.encode('utf-8'))

                    # Read response from the characteristic
                    response = await client.read_gatt_char(CHARACTERISTIC_UUID)
                    print("Received from server:", response.decode('utf-8'))

try:
    asyncio.run(run_client())
except KeyboardInterrupt:
    print("Client stopped.")
