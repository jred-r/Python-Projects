from config import HOST_ADDRESS, HOST_PORT, QUEUE_SIZE, BUFFER_SIZE, TIME_OUT
import socket
from utils import parse_http_request, process_request


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
            headers = req_str.split("\r\n")
            http_req = parse_http_request(headers)
            http_res = process_request(http_req)
            print(
                f"Processed: {http_req.Method} from {client_addr[0]}:{client_addr[1]}"
            )
            client_socket.sendall(http_res.to_bytes())
            client_socket.close()

    def stop(self):
        self.server_socket.close()

    def __del__(self):
        self.stop()


if __name__ == "__main__":
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server stopping")
    finally:
        server.stop()
