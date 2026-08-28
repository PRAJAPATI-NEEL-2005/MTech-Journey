import socket

def calculateChecksum(data):
    checksum = 0

    for character in data:
        checksum = (checksum + ord(character)) & 0xFFFFFFFF

    return checksum


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverAddress = ("127.0.0.1", 8081)

while True:

    message = input("\nEnter message: ")

    if message == "exit":
        client.sendto("exit".encode(), serverAddress)
        break

    checksum = calculateChecksum(message)

    print("Checksum:", checksum)

    packet = str(checksum) + "|" + message

    choice = input("Introduce error? (y/n): ")

    if choice.lower() == "y":

        # Change the message after calculating checksum
        if len(message) > 0:
            message = "X" + message[1:]

        packet = str(checksum) + "|" + message

        print("Artificial error introduced!")

    client.sendto(packet.encode(), serverAddress)

    print("Packet sent.")

    response, address = client.recvfrom(1024)

    print("Server:", response.decode())

client.close()