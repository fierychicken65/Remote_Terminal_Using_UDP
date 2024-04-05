import socket
import os
import subprocess

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def start_server():
    server_ip = get_ip_address()
    server_port = 12345
    print(f"Server IP address is: {server_ip}")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        print(f"Server listening on {server_ip}:{server_port}")

        while True:
            data, client_address = server_socket.recvfrom(1024)
            command = data.decode()

            if command.lower() == 'exit':
                break
            elif command.lower() == 'getcwd':
                current_directory = os.getcwd()
                server_socket.sendto(current_directory.encode(), client_address)
            elif command.startswith('cd '):
                try:
                    new_directory = command.split(' ', 1)[1]
                    os.chdir(new_directory)
                    current_directory = os.getcwd()
                    
                except Exception as e:
                    server_socket.sendto(str(e).encode(), client_address)
            else:
                try:
                    result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as e:
                    result = e.output

                current_directory = os.getcwd()
                response = f"{current_directory}\n{result.decode()}"
                server_socket.sendto(response.encode(), client_address)

if __name__ == "__main__":
    start_server()
