import socket
import json

def udp_server():
    # udp 通信地址，IP+端口号
    udp_addr = ('192.168.20.59', 9999)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定端口
    udp_socket.bind(udp_addr)
 
    # 等待接收对方发送的数据
    print("UDP server is running and waiting for data...")
    while True:
        recv_data, addr = udp_socket.recvfrom(1024)  # 1024表示本次接收的最大字节数
        # 解析接收到的JSON数据
        try:
            data = json.loads(recv_data.decode("utf-8"))
            print("[From %s:%d] Received Data:" % (addr[0], addr[1]))
            print("Boxes:", data["boxes"])
            print("Scores:", data["scores"])
            print("Class IDs:", data["class_ids"])
        except json.JSONDecodeError:
            print("Received non-JSON data:", recv_data.decode("utf-8"))
        except KeyError:
            print("JSON data missing some keys:", recv_data.decode("utf-8"))
 
if __name__ == '__main__':
    udp_server()
