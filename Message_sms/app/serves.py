import socket
import toml

with open("config.toml", "r") as f:
    config = toml.load(f)

url_server = config["server"]["host"]
port_server = config["server"]["port"]
print("Conect server")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((url_server, port_server))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:

            data = conn.recv(4096)

            if not data:
                break
            conn.sendall(data)
            print(data)
