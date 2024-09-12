!python3 -m pip install pybluez

import bluetooth

# Create a Bluetooth socket
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# Bind the socket to a port
server_sock.bind(("", bluetooth.PORT_ANY))

# Start listening for connections
server_sock.listen(1)

# Get the port that the server is listening on
port = server_sock.getsockname()[1]

# Advertise the service
service_id = "00001101-0000-1000-8000-00805F9B34FB"  # UUID for Serial Port Profile (SPP)
service_name = "blue-wifi-networks"
service_classes = [service_id, bluetooth.SERIAL_PORT_CLASS]
profiles = [bluetooth.SERIAL_PORT_PROFILE]

bluetooth.advertise_service(
    server_sock,
    service_name,
    service_id,
    service_classes,
    profiles
)

print(f"Waiting for connection on RFCOMM channel {port}")

# Accept a connection
client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print("Received:", data.decode('utf-8'))
finally:
    client_sock.close()
    server_sock.close()

#############################################################

bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# Connect to the server
client_sock.connect((server_address, port))

try:
    while True:
        message = input("Enter message to send: ")
        if message.lower() == 'exit':
            break
        client_sock.send(message)
finally:
    client_sock.close()
##############################################################

import bluetooth

# Create a Bluetooth socket
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# Bind the socket to a port
server_sock.bind(("", bluetooth.PORT_ANY))

# Start listening for connections
server_sock.listen(1)

# Get the port that the server is listening on
port = server_sock.getsockname()[1]

# Advertise the service
service_id = "00001101-0000-1000-8000-00805F9B34FB"  # UUID for Serial Port Profile (SPP)
service_name = "blue-wifi-networks"
service_classes = [service_id, bluetooth.SERIAL_PORT_CLASS]
profiles = [bluetooth.SERIAL_PORT_PROFILE]

bluetooth.advertise_service(
    server_sock,
    service_name,
    service_id,
    service_classes,
    profiles
)

print(f"Waiting for connection on RFCOMM channel {port}")

# Accept a connection
client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print("Received:", data.decode('utf-8'))
        # Echo the data back to the client
        client_sock.send(data)
finally:
    client_sock.close()
    server_sock.close()

###############################################################

import bluetooth

# Define the server address and port
server_address = '00:11:22:33:44:55'  # Replace with the server's Bluetooth address
port = 1  # Replace with the server's port number (usually 1 for RFCOMM)

# Create a Bluetooth socket
client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# Connect to the server
client_sock.connect((server_address, port))

try:
    while True:
        message = input("Enter message to send: ")
        if message.lower() == 'exit':
            break
        client_sock.send(message)
        # Receive the response from the server (echoed data)
        data = client_sock.recv(1024)
        print("Received from server:", data.decode('utf-8'))
finally:
    client_sock.close()
