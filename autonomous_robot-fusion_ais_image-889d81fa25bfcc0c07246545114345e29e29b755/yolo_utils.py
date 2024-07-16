import cv2
import numpy as np
import math
from yolov8.config import YOLO_CLASS_NAMES
from yolov8.YOLOv8 import YOLOv8

def calculate_angle(near_edge_midpoint, bottom_center):
    dx = near_edge_midpoint[0] - bottom_center[0]
    dy = bottom_center[1] - near_edge_midpoint[1]
    angle = math.degrees(math.atan2(dx, dy))
    return angle

def find_nearest_edge_midpoint(box, bottom_center_x):
    x, y, w, h = box
    left_midpoint = (x, y + h // 2)
    right_midpoint = (x + w, y + h // 2)
    top_midpoint = (x + w // 2, y)
    distances = {
        "left": abs(left_midpoint[0] - bottom_center_x),
        "right": abs(right_midpoint[0] - bottom_center_x),
        "top": abs(top_midpoint[0] - bottom_center_x)
    }
    nearest_edge = min(distances, key=distances.get)
    return locals()[f"{nearest_edge}_midpoint"]


def detect_video_stream(stream_url, weights_path, detection_threshold, angle_mmsi_mapping, output_path):
    yolov8 = YOLOv8(weights_path, detection_threshold)
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("Error: Unable to open video stream.")
        return

    # 获取视频源的宽度、高度和帧率，以用于视频保存
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 定义视频编码器和创建VideoWriter对象
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        bottom_center = (width // 2, height)
        boxes, scores, class_ids = yolov8.detect_objects(frame)

        for box in boxes:
            x1, y1, x2, y2 = box
            box_coords = (x1, y1, x2-x1, y2-y1)
            nearest_edge_midpoint = find_nearest_edge_midpoint(box_coords, bottom_center[0])
            angle = calculate_angle(nearest_edge_midpoint, bottom_center)

            # 查找与当前检测角度最接近的MMSI
            closest_mmsi, min_diff = None, float('inf')
            for k, mmsi in angle_mmsi_mapping.items():
                diff = abs(float(k) - angle)
                if diff < min_diff:
                    min_diff = diff
                    closest_mmsi = mmsi

            if closest_mmsi and min_diff < 10:  # 如果角度差小于10度
                mmsi_info = f"MMSI: {closest_mmsi}"
                cv2.putText(frame, mmsi_info, (int((x1+x2)/2), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        # 将处理后的帧写入输出文件
        out.write(frame)

        cv2.imshow('YOLOv8 Detection with MMSI', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()  # 释放VideoWriter对象
    cv2.destroyAllWindows()