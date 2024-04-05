import socket

def start_client():
    server_ip = input("Enter IP address:")
    server_port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        print(f"Connecting to server at {server_ip}:{server_port}")

        while True:
            client_socket.sendto('getcwd'.encode(), (server_ip, server_port))
            current_directory, _ = client_socket.recvfrom(1024)
            command = input(f"\033[94m{current_directory.decode()} :\033[m ")

            if command.lower() == 'exit':
                client_socket.sendto(command.encode(), (server_ip, server_port))
                break
            elif command.startswith('cd '):
                client_socket.sendto(command.encode(), (server_ip, server_port))
            else:
                client_socket.sendto(command.encode(), (server_ip, server_port))
                result, _ = client_socket.recvfrom(1024)
                print(result.decode())

if __name__ == "__main__":
    start_client()
