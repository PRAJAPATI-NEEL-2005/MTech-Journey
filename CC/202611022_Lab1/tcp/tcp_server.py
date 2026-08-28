import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 8080))
server.listen(1)

print("TCP Server started...")
print("Waiting for client...")

client, address = server.accept()

print("Client connected!")

while True:
    question = client.recv(1024).decode()

    if not question:
        break

    if question == "exit":
        break

    answer = "Question not found."

    file = open("qa.txt", "r")

    for line in file:
        parts = line.strip().split("|", 1)

        if len(parts) == 2:
            storedQuestion = parts[0]
            storedAnswer = parts[1]

            if question == storedQuestion:
                answer = storedAnswer
                break

    file.close()

    print("Question:", question)
    print("Answer:", answer)

    client.send(answer.encode())

client.close()
server.close()