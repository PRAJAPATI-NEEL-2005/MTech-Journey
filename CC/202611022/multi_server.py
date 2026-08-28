# Multi-threaded TCP echo server.
# A dedicated acceptor thread waits for connections and spawns one worker
# thread per client, so several clients are served at the same time.
# A counter caps how many clients the server will admit.
import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 5050
MAX_CLIENTS = 3          # counter that limits the number of client threads

STUDENT = "Krushna Parmar"
ROLL = "202611032"

count_lock = threading.Lock()
clients_served = 0


def stamp():
    return time.strftime("%H:%M:%S")


def handle_client(conn, addr, cid):
    """Runs in its own thread: talks to exactly one client."""
    me = threading.current_thread().name
    print(f"[{stamp()}] [SERVER] {me} started for client #{cid} at {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:                      # client closed the socket
                break
            msg = data.decode().strip()
            print(f"[{stamp()}] [SERVER] {me} received {msg!r}")
            reply = f"{me} -> client #{cid}: ack {msg!r}"
            conn.sendall(reply.encode())
    print(f"[{stamp()}] [SERVER] {me} finished with client #{cid}")


def acceptor(server):
    """Runs in its own thread: its only job is to create client threads."""
    global clients_served
    while True:
        with count_lock:
            if clients_served >= MAX_CLIENTS:
                print(f"[{stamp()}] [SERVER] thread limit ({MAX_CLIENTS}) reached, "
                      f"not accepting any more clients")
                return
        conn, addr = server.accept()
        with count_lock:
            clients_served += 1
            cid = clients_served
        worker = threading.Thread(target=handle_client, args=(conn, addr, cid),
                                  name=f"Worker-{cid}")
        print(f"[{stamp()}] [SERVER] accepted client #{cid}, spawning {worker.name}")
        worker.start()


def main():
    print(f"[SERVER] IT457 Cloud Computing - Lab 2 | {STUDENT} | {ROLL}")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[{stamp()}] [SERVER] listening on {HOST}:{PORT}, max {MAX_CLIENTS} clients")

    # the hint: one thread whose job is to create the per-client threads
    dispatcher = threading.Thread(target=acceptor, args=(server,), name="Acceptor")
    dispatcher.start()
    dispatcher.join()

    for t in threading.enumerate():
        if t is not threading.current_thread():
            t.join()
    server.close()
    print(f"[{stamp()}] [SERVER] all {clients_served} clients handled, server closed")


if __name__ == "__main__":
    main()
