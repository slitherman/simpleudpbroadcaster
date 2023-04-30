import socket
import json

IP = ""
PORT = 14000
ADDRESS = (IP, PORT)
BUFFER_SIZE = 65535

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDRESS)

while True:
    print("[WAITING FOR DATA...]")
    data_chunks = []
    while True:
        data, address = sock.recvfrom(BUFFER_SIZE)
        if not data:
            break
        data_chunks.append(data)

    data = b''.join(data_chunks).decode('utf-8')
    print("[RECEIVED DATA]")
    data_dict = json.loads(data)
    print(f"Total: {data_dict['total']}")
    for item in data_dict['items']:
        print(f"Title: {item['title']}")
