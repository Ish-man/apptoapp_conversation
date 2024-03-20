import socket
import threading

HOST = '0.0.0.0'
PORT = 6000

clients = []

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            for c in clients:
                if c != client_socket:
                    c.send(data)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        clients.remove(client_socket)
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server.accept()
            clients.append(client_socket)
            print(f"[*] Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("[*] Server shutting down.")
        server.close()

if __name__ == "__main__":
    start_server()
