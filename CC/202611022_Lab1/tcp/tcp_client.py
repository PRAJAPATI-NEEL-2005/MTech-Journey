import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 8080))

print("Connected to server!")

while True:
    
    question = input("\nEnter question: ")

    client.send(question.encode())

    if question == "exit":
        break

    answer = client.recv(1024).decode()

    print("Server:", answer)

client.close()