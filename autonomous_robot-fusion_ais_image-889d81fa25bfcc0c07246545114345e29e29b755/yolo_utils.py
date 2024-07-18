import cv2
import numpy as np
import math
import heapq
from yolov8.config import YOLO_CLASS_NAMES
from yolov8.YOLOv8 import YOLOv8



def initialize_video_stream(stream_url, weights_path, detection_threshold, output_path):
    yolov8 = YOLOv8(weights_path, detection_threshold)
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("Error: Unable to open video stream.")
        return None, None

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    return cap, yolov8, out

def process_frame(frame, width, height, yolov8, angle_mmsi_mapping, distance_mmsi_mapping, matched_angles):
    bottom_center = (width // 2, height)
    boxes, scores, class_ids = yolov8.detect_objects(frame)
    annotations = []

    for box in boxes:
        x1, y1, x2, y2 = box
        mmsi_info, distance_info = match_mmsi_and_distance((x1, y1, x2, y2), bottom_center, angle_mmsi_mapping, distance_mmsi_mapping, matched_angles)
        annotations.append((mmsi_info, distance_info, (x1, y1, x2, y2)))

    return annotations

def display_and_save_frame(frame, annotations, out):
    for mmsi_info, distance_info, (x1, y1, x2, y2) in annotations:
        cv2.putText(frame, mmsi_info, (int(x1), int(y1) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, distance_info, (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    out.write(frame)
    cv2.imshow('Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return False
    return True

def calculate_angle(near_edge_midpoint, bottom_center):
    dx = near_edge_midpoint[0] - bottom_center[0]
    dy = bottom_center[1] - near_edge_midpoint[1]
    angle = math.degrees(math.atan2(dx, dy))
    return angle

def match_mmsi_and_distance(box, bottom_center, angle_mmsi_mapping, distance_mmsi_mapping, matched_angles):
    x1, y1, x2, y2 = box
    mmsi_info = "Unknown MMSI"
    distance_info = "Unknown Distance"
    closest_mmsi = None
    closest_distance = float('inf')

    # 计算检测对象的中心点
    object_center = ((x1 + x2) // 2, (y1 + y2) // 2)

    # 计算对象中心与视频下边缘中心的角度
    angle = calculate_angle(object_center, bottom_center)

    # 查找与当前角度最接近的MMSI
    angle_diffs = [(abs(angle - k), mmsi) for k, mmsi in angle_mmsi_mapping.items() if k not in matched_angles]
    closest_five = heapq.nsmallest(5, angle_diffs)  # 获取最接近的五个角度

    for diff, mmsi in closest_five:
        if mmsi in distance_mmsi_mapping:
            curr_distance = distance_mmsi_mapping[mmsi]
            if curr_distance < closest_distance:
                closest_distance = curr_distance
                closest_mmsi = mmsi

    # 更新已匹配角度集合和返回信息
    if closest_mmsi:
        matched_angles.add(angle)  # 将当前角度标记为已匹配
        mmsi_info = f"MMSI: {closest_mmsi}"
        distance_info = f"Distance: {closest_distance:.2f} m"

    return mmsi_info, distance_info
