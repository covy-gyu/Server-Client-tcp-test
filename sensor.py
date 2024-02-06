import socket
import time
import random


def generate_sensor_data():
    # 센서 데이터 생성 로직 (임의 데이터 생성 예시)
    temperature = random.uniform(20.0, 30.0)
    humidity = random.uniform(30.0, 60.0)
    # return f"Temperature: {temperature:.2f}, Humidity: {humidity:.2f}"
    return "sensor1:temperature_data"


def sensor_client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            data = generate_sensor_data()
            s.sendall(data.encode())
            time.sleep(0.01)  # 데이터 전송 간격 조절 (0.01초마다 전송)


if __name__ == "__main__":
    HOST = "127.0.0.1"  # 예: '127.0.0.1'
    PORT = 65432  # 클라이언트 포트 번호
    sensor_client(HOST, PORT)
