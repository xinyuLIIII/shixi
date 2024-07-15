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
    if nearest_edge == "left":
        return left_midpoint
    elif nearest_edge == "right":
        return right_midpoint
    else:
        return top_midpoint

def test_detect(img_path):
    YOLOV8_WEIGHTS = "onnx/ship_yolov8.onnx"  
    DET_THRES = 0.35
    yolov8 = YOLOv8(YOLOV8_WEIGHTS, DET_THRES)
    
    cv_img = cv2.imread(img_path)
    if cv_img is None:
        raise ValueError("Image not found or unable to open.")
    
    height, width, _ = cv_img.shape
    
    # 检测物体
    boxes, scores, class_ids = yolov8.detect_objects(cv_img)
    
    # 打印识别到的物体坐标
    for box, score, class_id in zip(boxes, scores, class_ids):
        print(f"Class: {YOLO_CLASS_NAMES[class_id]}, Score: {score:.2f}, Box: {box}")

    bottom_center = (width // 2, height)
    angles = []
    for box in boxes:
        x1, y1, x2, y2 = box
        box_coords = (x1, y1, x2-x1, y2-y1)
        nearest_edge_midpoint = find_nearest_edge_midpoint(box_coords, bottom_center[0])
        angle = calculate_angle(nearest_edge_midpoint, bottom_center)
        angles.append(angle)
    
    return angles
    
if __name__ == '__main__':
    img_path = "onnx/test_det.png"  
    try:
        angles = test_detect(img_path)
        for i, angle in enumerate(angles):
            print(f"Angle for box {i+1}: {angle} degrees")
    except Exception as e:
        print(f"An error occurred: {e}")
