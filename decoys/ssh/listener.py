import socket
from concurrent.futures import ThreadPoolExecutor
from storage.event_recorder import create_event, save_event


def handle_session(conn, addr):
    with conn:
        conn.settimeout(10)
        try:
            data = conn.recv(1024)
            if data:
                client_id = data.decode("utf-8", errors="replace").strip()
                print(f"SSH Client Identification: {client_id}")

                if client_id.startswith("SSH-"):
                    event = create_event(
                        addr, PORT, "ssh_identification",
                        ssh_client=client_id
                    )
                    save_event(event)

                conn.sendall(b"SSH-2.0-HoneypotIntel_0.1\r\n")

        except socket.timeout:
            print(f"Session timed out: {addr}")

HOST = "127.0.0.1"
PORT = 2222

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"SSH decoy listening on {HOST}:{PORT}")
    with ThreadPoolExecutor(max_workers=5) as pool:
        while True:
            conn, addr = server.accept()
            pool.submit(handle_session, conn, addr)