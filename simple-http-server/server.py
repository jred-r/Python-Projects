from config import HOST_ADDRESS, HOST_PORT, QUEUE_SIZE, BUFFER_SIZE, TIME_OUT
import socket

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST_ADDRESS, HOST_PORT))
        self.server_socket.listen(QUEUE_SIZE)
        print(f"server listening on {HOST_ADDRESS}:{HOST_PORT}")

    def start(self):
        while True:
            self.server_socket.settimeout(TIME_OUT)
            try:
                client_socket, client_addr = self.server_socket.accept()
            except:
                continue
            req_bytes = client_socket.recv(BUFFER_SIZE)
            req_str: str = req_bytes.decode()
            headers = req_str.split('\r\n')
            first_header = headers[0].split(' ')
            method = first_header[0]
            req_path = first_header[1]
            print(f'Client addr {client_addr[0]}, method: {method}, path: {req_path}')

            with open('static/index.html') as fin:
                content = fin.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{content}"
            client_socket.sendall(response.encode())
            client_socket.close()
    
    def stop(self):
        self.server_socket.close()
    
    def __del__(self):
        self.stop()

if __name__ == "__main__":
    server =  Server()
    try:
        server.start()
    except KeyboardInterrupt:
        print('Server stopping')
    finally:
        server.stop()
        