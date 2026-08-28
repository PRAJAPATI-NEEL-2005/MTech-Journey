import socket

def calculateChecksum(data):
    checksum = 0

    for character in data:
        checksum = (checksum + ord(character)) & 0xFFFFFFFF

    return checksum


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind(("127.0.0.1", 8081))

print("UDP Server started...")
print("Waiting for packets...")

while True:

    data, address = server.recvfrom(1024)

    packet = data.decode()

    if packet == "exit":
        break

    parts = packet.split("|", 1)

    if len(parts) != 2:
        server.sendto(
            "ERROR: Invalid packet".encode(),
            address
        )
        continue

    receivedChecksum = int(parts[0])
    message = parts[1]

    calculatedChecksum = calculateChecksum(message)

    print("\nReceived message:", message)
    print("Received checksum:", receivedChecksum)
    print("Calculated checksum:", calculatedChecksum)

    if receivedChecksum == calculatedChecksum:

        print("Checksum matched.")
        print("Packet accepted.")

        response = "Packet accepted."

    else:

        print("Checksum mismatch!")
        print("Packet rejected.")

        response = "ERROR: Packet corrupted. Checksum mismatch."

    server.sendto(response.encode(), address)

server.close()