import socket
import threading

# Server configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 6000

# List to store connected clients
clients = []

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(4096)  # Receive data in chunks of 512 bytes
            if not data:
                break
            # Broadcast received audio data to all connected clients, except the sender
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
