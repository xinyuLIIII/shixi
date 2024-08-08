from time import sleep
import socket
import json
import numpy as np

def udp_cilent(res):
    boxes, scores, class_ids = res
    
    # 将ndarray转换为普通列表
    boxes = boxes.tolist() if isinstance(boxes, np.ndarray) else boxes
    scores = scores.tolist() if isinstance(scores, np.ndarray) else scores
    class_ids = class_ids.tolist() if isinstance(class_ids, np.ndarray) else class_ids
    
    # 将数据转换为JSON字符串
    data = json.dumps({
        "boxes": boxes,
        "scores": scores,
        "class_ids": class_ids
    })
    
    # udp 通信地址，IP+端口号
    udp_addr = ('192.168.20.59', 9999)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
    # 发送数据到指定的ip和端口
    udp_socket.sendto(data.encode('utf-8'), udp_addr)
    print("Data sent")
 
    # 关闭套接字
    udp_socket.close()
 
if __name__ == '__main__':
    print("udp client ")