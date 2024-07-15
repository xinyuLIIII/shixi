import cv2
import numpy as np
import math
from yolov8.config import YOLO_CLASS_NAMES
from yolov8.YOLOv8 import YOLOv8
import pandas as pd

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
    YOLOV8_WEIGHTS = "onnx/ship_yolov8.onnx"  # 替换为你的模型路径
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
    
    return boxes, angles

def calculate_relative_positions(target_points, camera_para):
    lon_cam, lat_cam, shoot_hdir = camera_para
    results = []

    for index, row in target_points.iterrows():
        lon_v, lat_v = row['lon'], row['lat']
        D_abs = count_distance((lat_cam, lon_cam), (lat_v, lon_v))
        relative_angle = get_degree(lat_cam, lon_cam, lat_v, lon_v)
        Angle_hor = relative_angle - shoot_hdir
        if Angle_hor < -180:
            Angle_hor += 360
        elif Angle_hor > 180:
            Angle_hor -= 360
        hor_rad = radians(Angle_hor)
        X_w = D_abs * sin(hor_rad)
        Y_w = D_abs * cos(hor_rad)
        angle_with_x_axis = degrees(atan2(X_w, Y_w))
        results.append((lon_v, lat_v, D_abs, angle_with_x_axis))

    return pd.DataFrame(results, columns=['lon', 'lat', 'distance', 'angle_with_x_axis'])

def match_angles(img_angles, geo_angles, boxes):
    matched_results = []
    for geo_angle in geo_angles:
        min_diff = float('inf')
        matched_box = None
        for box, img_angle in zip(boxes, img_angles):
            diff = abs(img_angle - geo_angle)
            if diff < min_diff:
                min_diff = diff
                matched_box = box

        if min_diff <= 10:
            matched_results.append((matched_box, geo_angle))
        else:
            matched_results.append((None, geo_angle))
    return matched_results

if __name__ == '__main__':
    img_path = "onnx/test_det.png"
    camera_para = [112.7919317, 23.1366617, 350]  # 相机参数 (经度, 纬度, 水平朝向)
    target_points = pd.DataFrame({
        'lon': [112.7909867],
        'lat': [23.1404667]
    })
    
    try:
        # 图像计算的角度
        boxes, img_angles = test_detect(img_path)
        
        # 经纬度计算的角度
        geo_data = calculate_relative_positions(target_points, camera_para)
        geo_angles = geo_data['angle_with_x_axis'].tolist()
        
        # 匹配角度
        matches = match_angles(img_angles, geo_angles, boxes)
        
        for i, (box, geo_angle) in enumerate(matches):
            if box is not None:
                print(f"Geo angle {geo_angle:.2f} matches with box {box}")
            else:
                print(f"Geo angle {geo_angle:.2f} has no match")
    except Exception as e:
        print(f"An error occurred: {e}")
