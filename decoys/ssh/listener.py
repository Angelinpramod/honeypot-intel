import socket

HOST = "127.0.0.1"
PORT = 2222

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"SSH decoy listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        print(f"Visitor connected: {addr}")
        conn.close()