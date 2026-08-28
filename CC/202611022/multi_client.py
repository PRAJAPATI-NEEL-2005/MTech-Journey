# TCP client: sends a simple message to the server repeatedly, on its own,
# with a short pause between messages so the run spans a period of time.
import socket
import sys
import time

HOST = "127.0.0.1"
PORT = 5050
REPEATS = 4
GAP = 1.0                # seconds between messages

TAG = sys.argv[1] if len(sys.argv) > 1 else "A"


def stamp():
    return time.strftime("%H:%M:%S")


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"[{stamp()}] [CLIENT-{TAG}] connected to {HOST}:{PORT}")

    for i in range(1, REPEATS + 1):
        message = f"msg {i} from client {TAG}"
        client.sendall(message.encode())
        print(f"[{stamp()}] [CLIENT-{TAG}] sent    : {message}")
        reply = client.recv(1024).decode()
        print(f"[{stamp()}] [CLIENT-{TAG}] received: {reply}")
        time.sleep(GAP)

    client.close()
    print(f"[{stamp()}] [CLIENT-{TAG}] done, connection closed")


if __name__ == "__main__":
    main()
