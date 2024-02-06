import socket
import threading
import time

sensor_data_groups = {}


def handle_sensor_data(conn, addr):
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(16384).decode()
        if not data:
            break

        sensor_id, sensor_data = data.split(":")
        if sensor_id not in sensor_data_groups:
            sensor_data_groups[sensor_id] = []
        sensor_data_groups[sensor_id].append(sensor_data)


def send_data_to_server(server_host, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_host, server_port))
        print("Connected to the server.")

        while True:
            time.sleep(10)
            for sensor_id, data_group in list(sensor_data_groups.items()):
                if data_group:
                    data_packet = f"{sensor_id}:{','.join(data_group)}"
                    s.sendall(data_packet.encode())
                    sensor_data_groups[sensor_id] = []


def client_server():
    host = "localhost"
    port = 65432

    server_host = "localhost"
    server_port = 65433
    connection_thread = threading.Thread(
        target=send_data_to_server, args=(server_host, server_port)
    )
    connection_thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_sensor_data, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    client_server()
